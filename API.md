# API Documentation

## Base URL
```
https://sturgeon-ai-prod.vercel.app
```

## Authentication
Currently using demo mode. Production will use JWT tokens.

## Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-11-01T12:00:00",
  "version": "1.0.0"
}
```

### Search Opportunities
```
GET /api/opportunities/search?keywords=AI&limit=10
```

Response:
```json
{
  "success": true,
  "count": 2,
  "opportunities": [...]
}
```

### Search Grants
```
GET /api/grants/search?keywords=technology&limit=10
```

### Analyze Contract
```
POST /api/ai/analyze-contract
Content-Type: application/json

{
  "contract_id": "SAM-2024-001",
  "contract_text": "Contract requirements..."
}
```

### Generate Proposal
```
POST /api/ai/generate-proposal
Content-Type: application/json

{
  "contract_id": "SAM-2024-001",
  "requirements": "System requirements...",
  "company_info": "Company profile..."
}
```

### Match Opportunities
```
POST /api/ai/match-opportunities
Content-Type: application/json

{
  "company_profile": "Company description...",
  "keywords": ["AI", "cloud", "cybersecurity"]
}
```

### Get Analytics
```
GET /api/analytics/dashboard
```

## Error Handling

All endpoints return errors in this format:
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per IP
