"""
Sturgeon AI Analytics Dashboard - Configuration
Application settings and environment variables
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/sturgeon"
    
    # JWT Configuration
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    
    # Admin Authentication
    admin_bearer_token: str
    
    # API Keys
    openai_api_key: Optional[str] = None
    sam_gov_api_key: Optional[str] = None
    grants_gov_api_key: Optional[str] = None
    
    # Stripe
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    
    # Frontend
    frontend_url: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
