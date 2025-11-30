from sqlalchemy import Column, String, BigInteger, DateTime, Enum as SQLEnum
from datetime import datetime
import uuid
import enum
from ..db.database import Base

class FileType(str, enum.Enum):
    IMAGE = "image"
    TEXT = "text"

class EmbeddingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class File(Base):
    __tablename__ = "files"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(SQLEnum(FileType), nullable=False)
    mime_type = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    s3_bucket = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    embedding_status = Column(SQLEnum(EmbeddingStatus), default=EmbeddingStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

