"""
Configuration settings for Sturgeon AI Backend
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase Configuration
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # API Keys
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    sam_gov_api_key: Optional[str] = os.getenv("SAM_GOV_API_KEY")
    grants_gov_api_key: Optional[str] = os.getenv("GRANTS_GOV_API_KEY")
    
    # JWT Configuration
    jwt_secret: str = os.getenv("JWT_SECRET", "supersecretkey123")
    jwt_algorithm: str = "HS256"
    
    # Stripe Configuration
    stripe_secret_key: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    
    # Frontend URL
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables


# Global settings instance
settings = Settings()
