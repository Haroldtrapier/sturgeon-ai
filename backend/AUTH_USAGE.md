# Authentication & Security Usage Guide

## Overview

This module provides admin authentication and security utilities for the Sturgeon AI Analytics Dashboard API.

## Configuration

Set the required environment variables in your `.env` file:

```env
JWT_SECRET=your_jwt_secret_here
ADMIN_BEARER_TOKEN=your_admin_bearer_token_here
```

## Usage Examples

### Using verify_admin_token (Header-based)

```python
from fastapi import FastAPI, Depends, Header
from auth import verify_admin_token

app = FastAPI()

@app.get("/admin/dashboard")
async def admin_dashboard(admin_id: str = Depends(verify_admin_token)):
    """Protected admin endpoint using header-based authentication"""
    return {"message": f"Welcome admin: {admin_id}"}
```

**Request:**
```bash
curl -H "Authorization: Bearer your_admin_bearer_token_here" \
     http://localhost:8000/admin/dashboard
```

### Using get_current_admin (HTTPBearer)

```python
from fastapi import FastAPI, Depends
from auth import get_current_admin

app = FastAPI()

@app.get("/admin/users")
async def list_users(admin_id: str = Depends(get_current_admin)):
    """Protected admin endpoint using HTTPBearer security"""
    return {"message": f"User list accessed by: {admin_id}"}
```

**Request:**
```bash
curl -H "Authorization: Bearer your_admin_bearer_token_here" \
     http://localhost:8000/admin/users
```

### Using check_admin_access (Simple Check)

```python
from fastapi import FastAPI, Header, HTTPException
from auth import check_admin_access

app = FastAPI()

@app.get("/admin/stats")
async def get_stats(authorization: str = Header(None)):
    """Manual token validation"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    
    token = authorization.split(" ")[1] if " " in authorization else ""
    if not check_admin_access(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"stats": "admin statistics"}
```

## Security Features

1. **Bearer Token Authentication**: Uses industry-standard Bearer token format
2. **Structured Logging**: All authentication events are logged with structlog
3. **Custom Exception Handling**: AdminAuthError provides consistent error responses
4. **Multiple Authentication Methods**: Choose between header-based or HTTPBearer-based

## Error Handling

All authentication failures raise `AdminAuthError` with HTTP 401 status:

- Missing authorization header
- Invalid authentication scheme (non-Bearer)
- Invalid header format
- Invalid or expired token

## Best Practices

1. **Never commit tokens to version control**: Use environment variables
2. **Rotate tokens regularly**: Update ADMIN_BEARER_TOKEN periodically
3. **Use HTTPS in production**: Protect tokens in transit
4. **Monitor authentication logs**: Watch for suspicious activity
5. **Set strong secrets**: Use cryptographically secure random values

## Testing

Run the test suite:

```bash
cd backend
pytest test_auth.py -v
```

## Integration with Existing API

To add admin authentication to existing endpoints:

```python
from fastapi import Depends
from auth import verify_admin_token

# Add to any protected endpoint
@app.get("/protected-resource")
async def protected_route(admin_id: str = Depends(verify_admin_token)):
    # Your endpoint logic here
    return {"data": "sensitive information"}
```
