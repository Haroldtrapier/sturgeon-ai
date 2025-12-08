"""
Tests for authentication and security utilities
"""

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from unittest.mock import Mock
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from auth import AdminAuthError, verify_admin_token, get_current_admin, check_admin_access
from config import settings


class TestAdminAuthError:
    """Test AdminAuthError exception class"""
    
    def test_default_message(self):
        """Test AdminAuthError with default message"""
        error = AdminAuthError()
        assert error.status_code == 401
        assert error.detail == "Unauthorized access"
    
    def test_custom_message(self):
        """Test AdminAuthError with custom message"""
        error = AdminAuthError("Custom error message")
        assert error.status_code == 401
        assert error.detail == "Custom error message"


class TestVerifyAdminToken:
    """Test verify_admin_token function"""
    
    @pytest.mark.asyncio
    async def test_missing_authorization_header(self):
        """Test when authorization header is missing"""
        with pytest.raises(AdminAuthError) as exc_info:
            await verify_admin_token(authorization=None)
        assert exc_info.value.detail == "Missing authorization header"
    
    @pytest.mark.asyncio
    async def test_invalid_scheme(self):
        """Test when authorization scheme is not Bearer"""
        with pytest.raises(AdminAuthError) as exc_info:
            await verify_admin_token(authorization="Basic token123")
        assert exc_info.value.detail == "Invalid authentication scheme"
    
    @pytest.mark.asyncio
    async def test_invalid_header_format(self):
        """Test when authorization header format is invalid"""
        with pytest.raises(AdminAuthError) as exc_info:
            await verify_admin_token(authorization="InvalidFormat")
        assert exc_info.value.detail == "Invalid authorization header format"
    
    @pytest.mark.asyncio
    async def test_invalid_token(self):
        """Test when token is invalid"""
        with pytest.raises(AdminAuthError) as exc_info:
            await verify_admin_token(authorization="Bearer wrong_token")
        assert exc_info.value.detail == "Invalid admin token"
    
    @pytest.mark.asyncio
    async def test_valid_token(self):
        """Test when token is valid"""
        result = await verify_admin_token(
            authorization=f"Bearer {settings.admin_bearer_token}"
        )
        assert result == "admin"


class TestGetCurrentAdmin:
    """Test get_current_admin function"""
    
    @pytest.mark.asyncio
    async def test_invalid_credentials(self):
        """Test when credentials are invalid"""
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "wrong_token"
        
        with pytest.raises(AdminAuthError) as exc_info:
            await get_current_admin(credentials=mock_credentials)
        assert exc_info.value.detail == "Invalid admin credentials"
    
    @pytest.mark.asyncio
    async def test_valid_credentials(self):
        """Test when credentials are valid"""
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = settings.admin_bearer_token
        
        result = await get_current_admin(credentials=mock_credentials)
        assert result == "admin"


class TestCheckAdminAccess:
    """Test check_admin_access function"""
    
    def test_invalid_token(self):
        """Test when token is invalid"""
        result = check_admin_access("wrong_token")
        assert result is False
    
    def test_valid_token(self):
        """Test when token is valid"""
        result = check_admin_access(settings.admin_bearer_token)
        assert result is True
    
    def test_empty_token(self):
        """Test when token is empty"""
        result = check_admin_access("")
        assert result is False
