from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "SciNewsAI"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/scinewsai"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ]
    
    # External APIs
    ARXIV_API_URL: str = "http://export.arxiv.org/api/query"
    
    # AI/RAG Configuration
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Email Configuration
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@scinewsai.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
