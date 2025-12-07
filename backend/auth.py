"""
Authentication and authorization utilities
"""

from fastapi import HTTPException, status
from typing import Optional
import structlog

from config import settings

logger = structlog.get_logger()


async def verify_admin_token(authorization: Optional[str] = None):
    """
    Verify admin authentication token
    
    Args:
        authorization: Authorization header value (Bearer token)
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not authorization:
        logger.warning("missing_authorization_header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning("invalid_authorization_format", auth_header=authorization)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    
    # Verify token against configured admin token
    if token != settings.admin_token:
        logger.warning("invalid_admin_token", token_prefix=token[:10] if len(token) > 10 else token)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin token",
        )
    
    logger.info("admin_token_verified")
    return True
