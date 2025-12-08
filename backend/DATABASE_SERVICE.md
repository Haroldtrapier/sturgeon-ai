# Supabase Analytics Database Service

This module provides a comprehensive service layer for Supabase database operations, focusing on analytics data management for the Sturgeon AI platform.

## Files

- `config.py` - Configuration management using pydantic-settings
- `database_service.py` - Main service implementation with SupabaseService class
- `test_database_service.py` - Unit tests for the service

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Update your `.env` file with Supabase credentials:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key_here
SUPABASE_ANON_KEY=your_anon_key_here  # Optional
```

**Important**: Replace placeholder values with actual Supabase credentials. The service will detect placeholders and disable client initialization with a warning.

### 3. Database Schema

The service expects the following tables in your Supabase database:

#### `analytics_events` table
```sql
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    metadata JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX idx_analytics_events_timestamp ON analytics_events(timestamp);
```

#### `users` table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `contract_analyses` table
```sql
CREATE TABLE contract_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    results JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_contract_analyses_contract_id ON contract_analyses(contract_id);
CREATE INDEX idx_contract_analyses_user_id ON contract_analyses(user_id);
```

## Usage

### Import the Service

```python
from database_service import db_service
```

The `db_service` is a global singleton instance ready to use.

### Log Events

```python
# Log a user registration
await db_service.log_event(
    event_type="user_registration",
    user_id="user_123",
    session_id="session_456",
    metadata={"source": "web", "plan": "pro"}
)

# Log a search
await db_service.log_event(
    event_type="search",
    user_id="user_123",
    metadata={"search_term": "government contracts"}
)

# Log a payment
await db_service.log_event(
    event_type="payment",
    user_id="user_123",
    metadata={"amount": 29.99, "currency": "USD"}
)
```

### Get Analytics Data

```python
# Get total users
total_users = await db_service.get_total_users()

# Get active users in the last 30 days
active_users = await db_service.get_active_users(days=30)

# Get event count
search_count = await db_service.get_event_count(
    event_type="search",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31)
)

# Get revenue statistics
revenue = await db_service.get_revenue_stats(
    start_date=datetime(2024, 1, 1)
)
# Returns: {"total_revenue": 5999.70, "transaction_count": 201, "average_transaction": 29.85}

# Get top search terms
top_terms = await db_service.get_top_search_terms(limit=10)
# Returns: [{"term": "grants", "count": 150}, {"term": "rfp", "count": 120}, ...]

# Get user growth over time
growth = await db_service.get_user_growth(days=30)
# Returns: [{"date": "2024-01-01", "count": 5}, {"date": "2024-01-02", "count": 8}, ...]
```

### Analyze Contracts

```python
# Analyze a contract
result = await db_service.analyze_contract(
    contract_id="contract_789",
    user_id="user_123",
    contract_type="federal",
    metadata={"agency": "DoD", "value": 1000000}
)

# Returns:
# {
#     "contract_id": "contract_789",
#     "status": "completed",
#     "analysis_score": 0.85,
#     "risk_factors": ["No significant risks identified"],
#     "opportunities": ["Potential for cost reduction", "Favorable renewal terms available"],
#     "compliance_status": "compliant",
#     "processing_time_ms": 152,
#     "completed_at": "2024-01-15T10:30:00"
# }
```

**Note**: The contract analysis currently uses mock data. Replace the implementation with actual AI analysis (OpenAI, custom ML model, etc.).

### Health Check

```python
# Check database connectivity
is_healthy = await db_service.health_check()
if is_healthy:
    print("Database connection is healthy")
else:
    print("Database connection failed")
```

## Error Handling

The service handles errors gracefully:

- All methods catch exceptions and log them using structlog
- Query methods return safe defaults (0, empty list, empty dict) on error
- Methods that modify data (log_event, analyze_contract) raise exceptions to allow proper error handling

```python
try:
    await db_service.log_event("user_login", user_id="user_123")
except Exception as e:
    # Handle error (e.g., alert, retry, fallback)
    print(f"Failed to log event: {e}")
```

## Configuration

All configuration is managed through `config.py` using pydantic-settings:

```python
from config import settings

# Access configuration
print(settings.supabase_url)
print(settings.environment)  # development, staging, production
print(settings.jwt_secret)
```

## Testing

Run the test suite:

```bash
cd backend
python -m pytest test_database_service.py -v
```

Integration tests are skipped by default as they require actual Supabase credentials. To run them:

```bash
python -m pytest test_database_service.py -v -m "not skip"
```

## Performance Considerations

1. **Active Users Query**: Currently processes events in memory. For large datasets (>10k events), consider using a database view with `COUNT(DISTINCT user_id)`.

2. **Search Term Analysis**: Limited to `MAX_SEARCH_EVENTS_TO_ANALYZE` (1000) events to prevent memory issues. For more comprehensive analysis, implement server-side aggregation.

3. **Connection Pooling**: The Supabase client handles connection pooling automatically.

## Security

- Always use `SUPABASE_SERVICE_KEY` for server-side operations
- Never expose the service key to the frontend
- The service validates credentials on initialization
- Change the default `JWT_SECRET` in production environments

## Future Improvements

- [ ] Replace mock contract analysis with actual AI integration
- [ ] Implement caching for frequently accessed analytics
- [ ] Add rate limiting for analytics endpoints
- [ ] Create database views for common aggregations
- [ ] Add batch event logging for improved performance
- [ ] Implement event streaming for real-time analytics

## Support

For questions or issues:
1. Check the code comments in `database_service.py`
2. Review test examples in `test_database_service.py`
3. Consult the [Supabase Python client documentation](https://supabase.com/docs/reference/python)
