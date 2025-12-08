"""
Sturgeon AI Analytics Dashboard - Configuration
Configuration management using pydantic-settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/postgres"
    
    # JWT Configuration
    jwt_secret: str = "supersecretkey123changethis"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    
    # Admin Authentication
    admin_bearer_token: str = "admin_default_token_change_in_production"
    
    # Stripe
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    
    # Frontend
    frontend_url: str = "http://localhost:3000"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
