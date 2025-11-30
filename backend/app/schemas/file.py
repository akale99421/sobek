from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.file import FileType, EmbeddingStatus

class FileBase(BaseModel):
    filename: str
    file_type: FileType
    mime_type: str
    file_size: int

class FileCreate(FileBase):
    session_id: str
    s3_bucket: str
    s3_key: str

class FileResponse(FileBase):
    id: str
    session_id: str
    s3_bucket: str
    s3_key: str
    embedding_status: EmbeddingStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_type: FileType
    file_size: int
    s3_path: str
    embedding_status: EmbeddingStatus
    message: str

class FileListResponse(BaseModel):
    files: list[FileResponse]
    total: int

