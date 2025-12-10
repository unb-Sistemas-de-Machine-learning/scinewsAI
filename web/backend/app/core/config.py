from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "SciNewsAI"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/scinewsai"
    
    # Supabase Configuration
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    USE_SUPABASE: bool = False
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:8080"
    
    # External APIs
    ARXIV_API_URL: str = "http://export.arxiv.org/api/query"
    
    # AI/RAG Configuration
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "bruno.martval@gmail.com"
    SMTP_PASSWORD: str = "ijwj bynm wbpn ogov"
    EMAIL_FROM: str = "bruno.martval@gmail.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
