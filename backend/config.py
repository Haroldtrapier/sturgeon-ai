"""
Application configuration and settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application settings
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Database settings
    database_url: Optional[str] = os.getenv("DATABASE_URL")
    
    # JWT settings
    jwt_secret: str = os.getenv("JWT_SECRET", "supersecretkey123")
    jwt_algorithm: str = "HS256"
    
    # Admin authentication
    admin_token: Optional[str] = os.getenv("ADMIN_TOKEN")
    
    # API settings
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow extra environment variables for other parts of the application
        # (e.g., STRIPE_SECRET_KEY, FRONTEND_URL used by main.py)
        extra = "ignore"


# Global settings instance
settings = Settings()
