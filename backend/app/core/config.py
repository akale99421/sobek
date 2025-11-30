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
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

