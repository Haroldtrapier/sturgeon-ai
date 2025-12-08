"""
Authentication and authorization utilities
"""

from fastapi import HTTPException, status
from typing import Optional
from config import settings
import structlog

logger = structlog.get_logger()


async def verify_admin_token(authorization: Optional[str] = None) -> None:
    """
    Verify admin authentication token
    
    Args:
        authorization: Authorization header value (format: "Bearer <token>")
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not authorization:
        logger.warning("admin_access_denied", reason="missing_authorization_header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning("admin_access_denied", reason="invalid_authorization_format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'"
        )
    
    token = parts[1]
    
    # Verify against admin token
    if not settings.admin_token:
        logger.error("admin_token_not_configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin authentication not configured"
        )
    
    if token != settings.admin_token:
        logger.warning("admin_access_denied", reason="invalid_token")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin token"
        )
    
    logger.info("admin_access_granted")
