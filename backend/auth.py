"""
Sturgeon AI Analytics Dashboard - Authentication & Security
Admin token verification and security utilities
"""

from fastapi import HTTPException, Security, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from config import settings
import structlog

logger = structlog.get_logger()

# Security scheme
security = HTTPBearer()


class AdminAuthError(HTTPException):
    """Custom exception for admin authentication failures"""
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=401, detail=detail)


async def verify_admin_token(
    authorization: Optional[str] = Header(None)
) -> str:
    """
    Verify admin access token from request header
    
    Args:
        authorization: Bearer token from request header
        
    Returns:
        user_id: Admin user identifier
        
    Raises:
        AdminAuthError: If token is invalid or missing
    """
    if not authorization:
        logger.warning("missing_authorization_header")
        raise AdminAuthError("Missing authorization header")
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise AdminAuthError("Invalid authentication scheme")
    except ValueError:
        raise AdminAuthError("Invalid authorization header format")
    
    # Verify token against configured admin token
    if token != settings.admin_bearer_token:
        logger.warning("invalid_admin_token")
        raise AdminAuthError("Invalid admin token")
    
    logger.info("admin_authenticated")
    return "admin"


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Alternative admin verification using HTTPBearer security
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        user_id: Admin user identifier
        
    Raises:
        AdminAuthError: If token is invalid
    """
    token = credentials.credentials
    
    if token != settings.admin_bearer_token:
        logger.warning("invalid_admin_credentials")
        raise AdminAuthError("Invalid admin credentials")
    
    return "admin"


def check_admin_access(token: str) -> bool:
    """
    Simple boolean check for admin access
    
    Args:
        token: Bearer token to verify
        
    Returns:
        bool: True if token is valid, False otherwise
    """
    return token == settings.admin_bearer_token
