from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from ...db.database import get_db
from ...models.file import File as FileModel, EmbeddingStatus
from ...services.s3_service import s3_service
from ...services.embedding_service import embedding_service
from ...services.qdrant_service import qdrant_service
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/embeddings", tags=["embeddings"])

class EmbeddingGenerateRequest(BaseModel):
    file_ids: List[str]

class EmbeddingStatusResponse(BaseModel):
    file_id: str
    filename: str
    status: EmbeddingStatus
    message: str

class ModelInfoResponse(BaseModel):
    text_model: str
    image_model: str
    embedding_dimension: int
    device: str
    text_model_loaded: bool
    image_model_loaded: bool

@router.post("/generate", response_model=List[EmbeddingStatusResponse])
async def generate_embeddings(
    request: EmbeddingGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate embeddings for specific files (on-demand)
    """
    if not request.file_ids:
        raise HTTPException(status_code=400, detail="No file IDs provided")
    
    results = []
    
    for file_id in request.file_ids:
        try:
            # Get file record
            file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
            
            if not file_record:
                results.append(EmbeddingStatusResponse(
                    file_id=file_id,
                    filename="unknown",
                    status=EmbeddingStatus.FAILED,
                    message="File not found"
                ))
                continue
            
            # Check if already processed
            if file_record.embedding_status == EmbeddingStatus.COMPLETED:
                results.append(EmbeddingStatusResponse(
                    file_id=file_id,
                    filename=file_record.filename,
                    status=EmbeddingStatus.COMPLETED,
                    message="Embedding already exists"
                ))
                continue
            
            # Update status to processing
            file_record.embedding_status = EmbeddingStatus.PROCESSING
            db.commit()
            
            # Download file from S3
            file_data = await s3_service.download_file(file_record.s3_key)
            
            # Generate embedding
            embedding = await embedding_service.embed_file(
                file_data=file_data,
                file_type=file_record.file_type.value,
                mime_type=file_record.mime_type
            )
            
            # Store in Qdrant
            metadata = {
                "file_id": file_id,
                "session_id": file_record.session_id,
                "filename": file_record.filename,
                "file_type": file_record.file_type.value,
                "mime_type": file_record.mime_type,
                "s3_bucket": file_record.s3_bucket,
                "s3_key": file_record.s3_key
            }
            
            await qdrant_service.store_embedding(
                file_id=file_id,
                embedding=embedding,
                metadata=metadata
            )
            
            # Update status to completed
            file_record.embedding_status = EmbeddingStatus.COMPLETED
            db.commit()
            
            results.append(EmbeddingStatusResponse(
                file_id=file_id,
                filename=file_record.filename,
                status=EmbeddingStatus.COMPLETED,
                message="Embedding generated successfully"
            ))
            
            logger.info(f"Generated embedding for file {file_id}")
        except Exception as e:
            logger.error(f"Failed to generate embedding for file {file_id}: {e}")
            
            # Update status to failed
            file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
            if file_record:
                file_record.embedding_status = EmbeddingStatus.FAILED
                db.commit()
            
            results.append(EmbeddingStatusResponse(
                file_id=file_id,
                filename=file_record.filename if file_record else "unknown",
                status=EmbeddingStatus.FAILED,
                message=f"Failed to generate embedding: {str(e)}"
            ))
    
    return results

@router.get("/status/{file_id}", response_model=EmbeddingStatusResponse)
async def get_embedding_status(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    Get embedding status for a specific file
    """
    file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    return EmbeddingStatusResponse(
        file_id=file_id,
        filename=file_record.filename,
        status=file_record.embedding_status,
        message=f"Embedding status: {file_record.embedding_status.value}"
    )

@router.get("/session/{session_id}/status", response_model=List[EmbeddingStatusResponse])
async def get_session_embedding_status(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get embedding status for all files in a session
    """
    files = db.query(FileModel).filter(FileModel.session_id == session_id).all()
    
    return [
        EmbeddingStatusResponse(
            file_id=f.id,
            filename=f.filename,
            status=f.embedding_status,
            message=f"Embedding status: {f.embedding_status.value}"
        )
        for f in files
    ]

@router.get("/models/info", response_model=ModelInfoResponse)
async def get_model_info():
    """
    Get information about loaded embedding models
    """
    info = embedding_service.get_model_info()
    return ModelInfoResponse(**info)

