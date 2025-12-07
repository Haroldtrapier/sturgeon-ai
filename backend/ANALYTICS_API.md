# Analytics Dashboard API Documentation

## Overview

The Analytics Dashboard API provides comprehensive business intelligence and operational metrics for the Sturgeon AI platform. All endpoints except `/health` require admin authentication using a Bearer token.

## Authentication

All protected endpoints require the `Authorization` header with a Bearer token:

```bash
Authorization: Bearer <ADMIN_TOKEN>
```

The `ADMIN_TOKEN` should be set in the `.env` file.

## Endpoints

### Health & Status

#### GET `/api/analytics/health`
**Public endpoint** - No authentication required

Returns system health status, database connectivity, and version information.

```bash
curl http://localhost:8000/api/analytics/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-07T20:00:00.000000",
  "version": "1.0.0",
  "database_connected": true,
  "services": {
    "api": "operational",
    "database": "operational",
    "analytics": "operational"
  }
}
```

#### GET `/api/analytics/status`
**Protected endpoint** - Requires admin authentication

Returns detailed system status and metrics.

```bash
curl -H "Authorization: Bearer <ADMIN_TOKEN>" \
  http://localhost:8000/api/analytics/status
```

### Metrics & Analytics

#### GET `/api/analytics/metrics?period=30d`
**Protected endpoint** - Requires admin authentication

Returns comprehensive analytics metrics for the specified period.

**Query Parameters:**
- `period`: Time period for metrics (`7d`, `30d`, `90d`, `365d`)

**Response includes:**
- User statistics (total, active, growth)
- Search metrics
- Contract analysis metrics
- Revenue data
- Conversion rates
- Top performing searches
- Revenue by day

```bash
curl -H "Authorization: Bearer <ADMIN_TOKEN>" \
  "http://localhost:8000/api/analytics/metrics?period=30d"
```

#### GET `/api/analytics/metrics/users`
**Protected endpoint** - Requires admin authentication

Returns detailed user analytics including retention rates.

```bash
curl -H "Authorization: Bearer <ADMIN_TOKEN>" \
  http://localhost:8000/api/analytics/metrics/users
```

### Contract Analysis

#### POST `/api/analytics/analyze-contract`
**Protected endpoint** - Requires admin authentication

Analyzes a government contract and returns risk assessment, opportunities, and recommendations.

**Request Body:**
```json
{
  "contract_id": "CONTRACT-123",
  "user_id": "user-456",
  "contract_type": "8a",
  "metadata": {
    "additional": "data"
  }
}
```

**Response:**
```json
{
  "contract_id": "CONTRACT-123",
  "analysis_id": "uuid",
  "risk_score": 35.5,
  "opportunities": ["..."],
  "compliance_issues": ["..."],
  "recommendations": ["..."],
  "estimated_value": 2500000.0,
  "analyzed_at": "2025-12-07T20:00:00.000000"
}
```

#### GET `/api/analytics/contracts/stats?days=30`
**Protected endpoint** - Requires admin authentication

Returns contract analysis statistics for the specified period.

```bash
curl -H "Authorization: Bearer <ADMIN_TOKEN>" \
  "http://localhost:8000/api/analytics/contracts/stats?days=30"
```

### Event Logging

#### POST `/api/analytics/events`
**Protected endpoint** - Requires admin authentication

Logs an analytics event for tracking user behavior and system events.

**Request Body:**
```json
{
  "event_type": "user_login",
  "user_id": "user-123",
  "session_id": "session-abc",
  "metadata": {
    "ip": "192.168.1.1"
  }
}
```

### Search Analytics

#### GET `/api/analytics/searches/top-terms?limit=20`
**Protected endpoint** - Requires admin authentication

Returns the most popular search terms with frequency counts.

**Query Parameters:**
- `limit`: Number of top terms to return (default: 20)

```bash
curl -H "Authorization: Bearer <ADMIN_TOKEN>" \
  "http://localhost:8000/api/analytics/searches/top-terms?limit=10"
```

## Environment Variables

Required environment variables in `.env`:

```bash
# Admin API Authentication
ADMIN_TOKEN=your-admin-token-change-in-production

# Database (optional for mock implementation)
DATABASE_URL=postgresql://...

# Other configurations
ENVIRONMENT=development
DEBUG=true
```

## Error Responses

### 401 Unauthorized
Missing or invalid authorization header:
```json
{
  "detail": "Authorization header is required"
}
```

### 403 Forbidden
Invalid admin token:
```json
{
  "detail": "Invalid admin token"
}
```

### 500 Internal Server Error
Server error with details:
```json
{
  "detail": "Error message describing the issue"
}
```

## Testing

All endpoints can be tested using curl or any HTTP client. Example test script:

```bash
#!/bin/bash
TOKEN="your-admin-token"
BASE_URL="http://localhost:8000/api/analytics"

# Test health (public)
curl -s ${BASE_URL}/health | python -m json.tool

# Test metrics (authenticated)
curl -s -H "Authorization: Bearer ${TOKEN}" \
  "${BASE_URL}/metrics?period=30d" | python -m json.tool

# Test contract analysis (authenticated)
curl -s -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"contract_id":"TEST-001","user_id":"user-789"}' \
  ${BASE_URL}/analyze-contract | python -m json.tool
```

## Implementation Notes

- The current implementation uses a mock database service that returns simulated data
- In production, the `database.py` module should be updated to connect to a real database
- All timestamps are in UTC
- Structured logging is implemented using `structlog` for better log analysis
- All endpoints return JSON responses
