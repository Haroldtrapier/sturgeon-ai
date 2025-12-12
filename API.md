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

## Marketing ROI Calculator Endpoints

### Calculate Campaign ROI
```
POST /marketing/calculate-roi
Content-Type: application/json

{
  "channel": "linkedin_ads",
  "budget": 10000,
  "duration_months": 3
}
```

Response:
```json
{
  "channel": "linkedin_ads",
  "investment": {
    "budget": 10000,
    "duration_months": 3,
    "monthly_spend": 3333.33
  },
  "performance": {
    "clicks": 1818,
    "leads": 90,
    "demos_booked": 27,
    "customers_acquired": 6,
    "revenue_generated": 14328
  },
  "efficiency_metrics": {
    "cac": 1666.67,
    "ltv": 5970.0,
    "ltv_cac_ratio": 3.58,
    "payback_period_months": 8.4
  },
  "returns": {
    "roi_percentage": 43.3,
    "roas": 1.43,
    "profit": 4328.0,
    "break_even_customers": 4
  },
  "recommendation": "OPTIMIZE: Profitable but suboptimal. Test new creative and audiences."
}
```

Supported channels: `linkedin_ads`, `google_ads`, `content_marketing`, `email_marketing`

### Optimize Budget Allocation
```
POST /marketing/optimize-budget
Content-Type: application/json

{
  "total_budget": 30000,
  "channels": ["linkedin_ads", "google_ads", "content_marketing"]
}
```

Response:
```json
{
  "total_budget": 30000,
  "optimized_allocation": {
    "content_marketing": {
      "budget": 18000,
      "percentage": 60.0,
      "expected_customers": 54,
      "expected_revenue": 128952,
      "roi": 616.4
    },
    "google_ads": {
      "budget": 9000,
      "percentage": 30.0,
      "expected_customers": 14,
      "expected_revenue": 33432,
      "roi": 271.5
    },
    "linkedin_ads": {
      "budget": 3000,
      "percentage": 10.0,
      "expected_customers": 2,
      "expected_revenue": 4776,
      "roi": 59.2
    }
  },
  "channel_ranking": ["content_marketing", "google_ads", "linkedin_ads"],
  "total_expected_results": {
    "customers": 70,
    "revenue": 167160,
    "roi": 457.2,
    "average_cac": 428.57
  },
  "execution_priority": [
    "1. Launch content_marketing with $18,000 (highest ROI)",
    "2. Add google_ads with $9,000 after 30 days",
    "3. Test linkedin_ads with $3,000 after 60 days"
  ]
}
```

### Project Growth Trajectory
```
POST /marketing/project-growth
Content-Type: application/json

{
  "monthly_budget": 5000,
  "duration_months": 12,
  "channel_mix": {
    "linkedin_ads": 0.40,
    "content_marketing": 0.30,
    "email_marketing": 0.20,
    "google_ads": 0.10
  }
}
```

Response includes monthly breakdown and year-end totals with MRR projections.

### Get Marketing Benchmarks
```
GET /marketing/benchmarks
```

Response:
```json
{
  "benchmarks": {
    "linkedin_ads": {
      "cpc": 5.5,
      "ctr": 0.025,
      "conversion_rate": 0.05,
      "avg_deal_size": 2388
    },
    "google_ads": {
      "cpc": 3.75,
      "ctr": 0.035,
      "conversion_rate": 0.08,
      "avg_deal_size": 2388
    },
    "content_marketing": {
      "cost_per_article": 500,
      "traffic_per_article": 1000,
      "conversion_rate": 0.02,
      "avg_deal_size": 2388
    },
    "email_marketing": {
      "cost_per_send": 0.01,
      "open_rate": 0.25,
      "click_rate": 0.05,
      "conversion_rate": 0.08,
      "avg_deal_size": 2388
    }
  }
}
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
