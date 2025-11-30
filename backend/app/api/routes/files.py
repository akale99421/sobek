from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import uuid
import logging
from ...db.database import get_db
from ...models.file import File as FileModel, FileType, EmbeddingStatus
from ...schemas.file import FileUploadResponse, FileResponse, FileListResponse
from ...services.s3_service import s3_service
from ...services.embedding_service import embedding_service
from ...services.qdrant_service import qdrant_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/files", tags=["files"])

def determine_file_type(mime_type: str) -> FileType:
    """Determine if file is image or text based on MIME type"""
    if mime_type.startswith("image/"):
        return FileType.IMAGE
    else:
        return FileType.TEXT

async def process_embedding_background(
    file_id: str,
    s3_key: str,
    file_type: FileType,
    mime_type: str,
    db: Session
):
    """Background task to generate and store embedding"""
    try:
        # Update status to processing
        file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
        if file_record:
            file_record.embedding_status = EmbeddingStatus.PROCESSING
            db.commit()
        
        # Download file from S3
        file_data = await s3_service.download_file(s3_key)
        
        # Generate embedding
        embedding = await embedding_service.embed_file(
            file_data=file_data,
            file_type=file_type.value,
            mime_type=mime_type
        )
        
        # Store in Qdrant
        metadata = {
            "file_id": file_id,
            "session_id": file_record.session_id,
            "filename": file_record.filename,
            "file_type": file_type.value,
            "mime_type": mime_type,
            "s3_bucket": file_record.s3_bucket,
            "s3_key": s3_key
        }
        
        await qdrant_service.store_embedding(
            file_id=file_id,
            embedding=embedding,
            metadata=metadata
        )
        
        # Update status to completed
        file_record.embedding_status = EmbeddingStatus.COMPLETED
        db.commit()
        
        logger.info(f"Successfully processed embedding for file {file_id}")
    except Exception as e:
        logger.error(f"Failed to process embedding for file {file_id}: {e}")
        # Update status to failed
        file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
        if file_record:
            file_record.embedding_status = EmbeddingStatus.FAILED
            db.commit()

@router.post("/upload", response_model=List[FileUploadResponse])
async def upload_files(
    session_id: str,
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload multiple files, store in S3, and trigger embedding generation
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    uploaded_files = []
    
    for file in files:
        try:
            # Generate unique file ID
            file_id = str(uuid.uuid4())
            
            # Determine file type
            mime_type = file.content_type or "application/octet-stream"
            file_type = determine_file_type(mime_type)
            
            # Read file content
            file_content = await file.read()
            file_size = len(file_content)
            
            # Generate S3 key
            s3_key = f"{session_id}/{file_id}/{file.filename}"
            
            # Upload to S3
            s3_path = await s3_service.upload_file(
                file_data=file_content,
                object_key=s3_key,
                content_type=mime_type
            )
            
            # Create database record
            file_record = FileModel(
                id=file_id,
                session_id=session_id,
                filename=file.filename,
                file_type=file_type,
                mime_type=mime_type,
                file_size=file_size,
                s3_bucket=s3_path.split('/')[0],
                s3_key=s3_key,
                embedding_status=EmbeddingStatus.PENDING
            )
            
            db.add(file_record)
            db.commit()
            db.refresh(file_record)
            
            # Schedule background embedding generation
            background_tasks.add_task(
                process_embedding_background,
                file_id=file_id,
                s3_key=s3_key,
                file_type=file_type,
                mime_type=mime_type,
                db=db
            )
            
            uploaded_files.append(FileUploadResponse(
                file_id=file_id,
                filename=file.filename,
                file_type=file_type,
                file_size=file_size,
                s3_path=s3_path,
                embedding_status=EmbeddingStatus.PENDING,
                message="File uploaded successfully, embedding generation in progress"
            ))
            
            logger.info(f"Uploaded file {file.filename} with ID {file_id}")
        except Exception as e:
            logger.error(f"Failed to upload file {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
    
    return uploaded_files

@router.get("/session/{session_id}", response_model=FileListResponse)
async def get_session_files(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all files for a session
    """
    files = db.query(FileModel).filter(FileModel.session_id == session_id).all()
    
    return FileListResponse(
        files=[FileResponse.model_validate(f) for f in files],
        total=len(files)
    )

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    Get file details by ID
    """
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse.model_validate(file)

@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a file and its embedding
    """
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Delete from S3
        await s3_service.delete_file(file.s3_key)
        
        # Delete from Qdrant
        await qdrant_service.delete_embedding(file_id)
        
        # Delete from database
        db.delete(file)
        db.commit()
        
        return {"message": "File deleted successfully", "file_id": file_id}
    except Exception as e:
        logger.error(f"Failed to delete file {file_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

