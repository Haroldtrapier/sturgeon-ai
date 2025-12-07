"""
Tests for authentication and security utilities
"""

import pytest
from fastapi import Header
from fastapi.security import HTTPAuthorizationCredentials
from auth import (
    AdminAuthError,
    verify_admin_token,
    get_current_admin,
    check_admin_access
)
from config import settings


# Test helper
class MockCredentials:
    """Mock HTTPAuthorizationCredentials for testing"""
    def __init__(self, token):
        self.credentials = token


@pytest.mark.asyncio
async def test_verify_admin_token_success():
    """Test successful admin token verification"""
    auth_header = f"Bearer {settings.admin_bearer_token}"
    result = await verify_admin_token(authorization=auth_header)
    assert result == "admin"


@pytest.mark.asyncio
async def test_verify_admin_token_missing_header():
    """Test verification fails when authorization header is missing"""
    with pytest.raises(AdminAuthError) as exc_info:
        await verify_admin_token(authorization=None)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Missing authorization header"


@pytest.mark.asyncio
async def test_verify_admin_token_invalid_scheme():
    """Test verification fails with invalid authentication scheme"""
    auth_header = f"Basic {settings.admin_bearer_token}"
    with pytest.raises(AdminAuthError) as exc_info:
        await verify_admin_token(authorization=auth_header)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid authentication scheme"


@pytest.mark.asyncio
async def test_verify_admin_token_invalid_format():
    """Test verification fails with invalid header format"""
    auth_header = "InvalidFormatNoSpace"
    with pytest.raises(AdminAuthError) as exc_info:
        await verify_admin_token(authorization=auth_header)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid authorization header format"


@pytest.mark.asyncio
async def test_verify_admin_token_wrong_token():
    """Test verification fails with wrong token"""
    auth_header = "Bearer wrong_token_12345"
    with pytest.raises(AdminAuthError) as exc_info:
        await verify_admin_token(authorization=auth_header)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid admin token"


@pytest.mark.asyncio
async def test_get_current_admin_success():
    """Test successful admin verification using HTTPBearer"""
    credentials = MockCredentials(settings.admin_bearer_token)
    result = await get_current_admin(credentials=credentials)
    assert result == "admin"


@pytest.mark.asyncio
async def test_get_current_admin_invalid_credentials():
    """Test admin verification fails with invalid credentials"""
    credentials = MockCredentials("invalid_token")
    with pytest.raises(AdminAuthError) as exc_info:
        await get_current_admin(credentials=credentials)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid admin credentials"


def test_check_admin_access_valid():
    """Test check_admin_access returns True for valid token"""
    assert check_admin_access(settings.admin_bearer_token) is True


def test_check_admin_access_invalid():
    """Test check_admin_access returns False for invalid token"""
    assert check_admin_access("invalid_token") is False


def test_check_admin_access_empty():
    """Test check_admin_access returns False for empty token"""
    assert check_admin_access("") is False


def test_admin_auth_error_default():
    """Test AdminAuthError with default message"""
    error = AdminAuthError()
    assert error.status_code == 401
    assert error.detail == "Unauthorized access"


def test_admin_auth_error_custom():
    """Test AdminAuthError with custom message"""
    error = AdminAuthError(detail="Custom error message")
    assert error.status_code == 401
    assert error.detail == "Custom error message"
