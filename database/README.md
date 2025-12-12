# Database Schema Documentation

This directory contains database migration files for the Sturgeon AI platform using Supabase (PostgreSQL).

## Migration Files

### Core Schema
- `create_profiles_table.sql` - Company profile information for government contracting
- `create_opportunities_table.sql` - Government contract opportunities saved by users

### Analytics Schema
- `create_analytics_schema.sql` - Complete analytics dashboard database schema

## Analytics Dashboard Schema

The analytics schema provides comprehensive tracking and reporting capabilities for the Sturgeon AI platform.

### Tables

#### 1. analytics_events
Tracks all user interaction events for analytics purposes.
- **Columns**: event_type, user_id, session_id, metadata (JSONB), timestamp
- **Use Cases**: User behavior tracking, feature usage, interaction patterns
- **Indexes**: event_type, user_id, timestamp (DESC), metadata (GIN)

#### 2. analytics_users
Extended user information specifically for analytics dashboard.
- **Columns**: email, full_name, company, role, last_login, is_active
- **Use Cases**: User demographics, account management, user segmentation
- **Indexes**: email, created_at (DESC)

#### 3. contract_analyses
Tracks contract analysis results and metrics.
- **Columns**: contract_id, user_id, contract_type, results (JSONB), status
- **Use Cases**: Contract processing metrics, AI analysis tracking, success rates
- **Indexes**: contract_id, user_id, created_at (DESC), results (GIN)

#### 4. user_sessions
User session tracking for engagement analytics.
- **Columns**: session_id, user_id, started_at, ended_at, duration_seconds, page_views, actions_count
- **Use Cases**: Session analytics, engagement metrics, user activity patterns
- **Indexes**: user_id, started_at (DESC)

#### 5. revenue_events
Revenue and transaction tracking for business metrics.
- **Columns**: user_id, transaction_id, amount, currency, product_type, subscription_tier
- **Use Cases**: Revenue tracking, subscription analytics, financial reporting
- **Indexes**: user_id, created_at (DESC), amount

#### 6. system_metrics
System performance and health monitoring metrics.
- **Columns**: metric_type, metric_value, unit, metadata (JSONB)
- **Use Cases**: Performance monitoring, system health, operational metrics
- **Indexes**: metric_type, recorded_at (DESC)

### Views

#### daily_active_users
Provides daily active user counts.
```sql
SELECT date, active_users FROM daily_active_users;
```

#### revenue_summary
Summarizes revenue by date, product type, and subscription tier.
```sql
SELECT date, transaction_count, total_revenue, avg_transaction_value 
FROM revenue_summary;
```

#### contract_analysis_summary
Aggregates contract analysis metrics by date and user.
```sql
SELECT date, total_analyses, user_id, scores 
FROM contract_analysis_summary;
```

### Security

All tables have Row Level Security (RLS) enabled with policies that grant full access to the service role. This ensures:
- Secure access control at the database level
- Service-level operations can manage all data
- Future user-level policies can be added as needed

### Sample Data

The migration includes sample users for testing:
- `admin@trapier.com` - Harold Trapier (Trapier Management LLC)
- `demo@government.gov` - Demo User (Department of Defense)

## Setup Instructions

### Running Migrations

1. **Via Supabase Dashboard**:
   - Navigate to the SQL Editor in your Supabase project
   - Copy the contents of the migration file
   - Execute the SQL

2. **Via Supabase CLI**:
   ```bash
   supabase migration new create_analytics_schema
   # Copy the migration file contents
   supabase db push
   ```

3. **Direct Database Access**:
   ```bash
   psql $DATABASE_URL -f database/migrations/create_analytics_schema.sql
   ```

### Verification

After running the migration, verify the tables were created:

```sql
-- Check tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE '%analytics%' OR table_name IN ('contract_analyses', 'user_sessions', 'revenue_events', 'system_metrics');

-- Check views
SELECT table_name FROM information_schema.views 
WHERE table_schema = 'public';

-- Check RLS policies
SELECT tablename, policyname FROM pg_policies 
WHERE tablename IN ('analytics_events', 'analytics_users', 'contract_analyses', 'user_sessions', 'revenue_events', 'system_metrics');
```

## Maintenance

### Updating Timestamps

The schema includes automatic timestamp updates via triggers:
- `analytics_users.updated_at` - Updated on any row modification
- `contract_analyses.updated_at` - Updated on any row modification

### Adding Indexes

When adding new queries or improving performance, consider adding indexes:
```sql
CREATE INDEX idx_name ON table_name(column_name);
CREATE INDEX idx_name ON table_name USING GIN(jsonb_column); -- For JSONB columns
```

### Monitoring Performance

Use the `system_metrics` table to track database and application performance:
```sql
INSERT INTO system_metrics (metric_type, metric_value, unit, metadata)
VALUES ('query_duration', 1.234, 'seconds', '{"query": "SELECT * FROM analytics_events"}'::jsonb);
```

## Best Practices

1. **Use JSONB for Flexible Data**: The `metadata` columns use JSONB for flexible schema-free data storage
2. **Index Strategy**: GIN indexes are used for JSONB columns, B-tree for standard lookups
3. **Timestamp Conventions**: Use TIMESTAMPTZ for all time-related fields
4. **UUID Primary Keys**: All tables use UUID v4 for primary keys
5. **Row Level Security**: Always keep RLS enabled for security

## Integration

### Backend Integration

Example usage in backend code:

```javascript
// Track an event
await supabase
  .from('analytics_events')
  .insert({
    event_type: 'contract_viewed',
    user_id: userId,
    session_id: sessionId,
    metadata: { contract_id: '123', source: 'dashboard' }
  });

// Record revenue
await supabase
  .from('revenue_events')
  .insert({
    user_id: userId,
    transaction_id: txId,
    amount: 99.99,
    product_type: 'subscription',
    subscription_tier: 'professional'
  });
```

### Analytics Queries

```sql
-- Daily active users over time
SELECT * FROM daily_active_users WHERE date >= CURRENT_DATE - INTERVAL '30 days';

-- Revenue trends
SELECT * FROM revenue_summary WHERE date >= CURRENT_DATE - INTERVAL '90 days';

-- Top events by type
SELECT event_type, COUNT(*) as count 
FROM analytics_events 
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY event_type 
ORDER BY count DESC;
```

## Support

For issues or questions about the database schema:
1. Check the Supabase documentation
2. Review the migration files in this directory
3. Contact the development team
