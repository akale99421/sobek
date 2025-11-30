from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Platinum Sequence"
    API_VERSION: str = "v1"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://platinumsequence.com",
        "https://www.platinumsequence.com"
    ]
    
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "platinumsequence"
    
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    
    # MinIO S3 Configuration
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "inventory-files"
    MINIO_SECURE: bool = False
    
    # ML Model Configuration
    TEXT_EMBEDDING_MODEL: str = "BAAI/bge-base-en-v1.5"
    IMAGE_EMBEDDING_MODEL: str = "facebook/dinov2-base"
    EMBEDDING_DIMENSION: int = 768
    DEVICE: str = "cpu"  # Set to "cuda" if GPU available
    
    # Qdrant Collection Configuration
    QDRANT_COLLECTION_NAME: str = "inventory_embeddings"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

