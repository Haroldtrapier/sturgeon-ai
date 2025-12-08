"""
Configuration settings for Sturgeon AI backend services
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase Configuration
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    supabase_anon_key: Optional[str] = os.getenv("SUPABASE_ANON_KEY", None)
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # JWT Configuration
    jwt_secret: str = os.getenv("JWT_SECRET", "supersecretkey123changethis")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Stripe Configuration
    stripe_secret_key: Optional[str] = os.getenv("STRIPE_SECRET_KEY", None)
    stripe_webhook_secret: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET", None)
    
    # Frontend Configuration
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
