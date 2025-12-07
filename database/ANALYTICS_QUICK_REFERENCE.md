# Analytics Dashboard - Quick Reference Guide

## Table Overview

| Table Name | Purpose | Key Columns |
|------------|---------|-------------|
| `analytics_events` | Track user interactions | event_type, user_id, session_id, metadata |
| `analytics_users` | Enhanced user profiles | email, full_name, company, role |
| `contract_analyses` | Contract processing metrics | contract_id, user_id, results |
| `user_sessions` | Session tracking | session_id, user_id, duration_seconds |
| `revenue_events` | Revenue tracking | user_id, transaction_id, amount |
| `system_metrics` | System monitoring | metric_type, metric_value |

## Common Queries

### User Activity

```sql
-- Daily active users for last 30 days
SELECT * FROM daily_active_users 
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY date DESC;

-- Events by type (last 7 days)
SELECT 
    event_type,
    COUNT(*) as count,
    COUNT(DISTINCT user_id) as unique_users
FROM analytics_events
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY event_type
ORDER BY count DESC;

-- User engagement metrics
SELECT 
    user_id,
    COUNT(*) as total_events,
    COUNT(DISTINCT session_id) as sessions,
    MIN(timestamp) as first_seen,
    MAX(timestamp) as last_seen
FROM analytics_events
WHERE user_id IS NOT NULL
GROUP BY user_id
ORDER BY total_events DESC;
```

### Session Analytics

```sql
-- Session duration distribution
SELECT 
    CASE 
        WHEN duration_seconds < 60 THEN '< 1 min'
        WHEN duration_seconds < 300 THEN '1-5 min'
        WHEN duration_seconds < 900 THEN '5-15 min'
        WHEN duration_seconds < 1800 THEN '15-30 min'
        ELSE '> 30 min'
    END as duration_bucket,
    COUNT(*) as session_count,
    AVG(page_views) as avg_page_views
FROM user_sessions
WHERE ended_at IS NOT NULL
GROUP BY duration_bucket
ORDER BY 
    CASE 
        WHEN duration_seconds < 60 THEN 1
        WHEN duration_seconds < 300 THEN 2
        WHEN duration_seconds < 900 THEN 3
        WHEN duration_seconds < 1800 THEN 4
        ELSE 5
    END;

-- Top active users by session count
SELECT 
    user_id,
    COUNT(*) as session_count,
    SUM(page_views) as total_page_views,
    AVG(duration_seconds) as avg_session_duration
FROM user_sessions
WHERE started_at >= NOW() - INTERVAL '30 days'
GROUP BY user_id
ORDER BY session_count DESC
LIMIT 10;
```

### Revenue Analytics

```sql
-- Revenue summary from view
SELECT * FROM revenue_summary
WHERE date >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY date DESC;

-- Monthly recurring revenue (MRR)
SELECT 
    DATE_TRUNC('month', created_at) as month,
    SUM(amount) as total_revenue,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_transaction_value
FROM revenue_events
WHERE subscription_tier IS NOT NULL
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- Revenue by product type
SELECT 
    product_type,
    subscription_tier,
    COUNT(*) as subscriptions,
    SUM(amount) as total_revenue
FROM revenue_events
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY product_type, subscription_tier
ORDER BY total_revenue DESC;

-- Customer lifetime value (simple)
SELECT 
    user_id,
    COUNT(*) as transactions,
    SUM(amount) as lifetime_value,
    MIN(created_at) as first_purchase,
    MAX(created_at) as last_purchase
FROM revenue_events
GROUP BY user_id
ORDER BY lifetime_value DESC
LIMIT 20;
```

### Contract Analysis Metrics

```sql
-- Contract analysis summary
SELECT * FROM contract_analysis_summary
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY date DESC;

-- Analysis success rate
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM contract_analyses
GROUP BY status
ORDER BY count DESC;

-- Average analysis by contract type
SELECT 
    contract_type,
    COUNT(*) as analyses_count,
    AVG((results->>'analysis_score')::numeric) as avg_score
FROM contract_analyses
WHERE results->>'analysis_score' IS NOT NULL
GROUP BY contract_type
ORDER BY analyses_count DESC;

-- Daily analysis volume
SELECT 
    DATE(created_at) as date,
    COUNT(*) as analyses,
    COUNT(DISTINCT user_id) as unique_users
FROM contract_analyses
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### System Monitoring

```sql
-- Recent system metrics
SELECT 
    metric_type,
    metric_value,
    unit,
    recorded_at
FROM system_metrics
ORDER BY recorded_at DESC
LIMIT 50;

-- Average metric values by type
SELECT 
    metric_type,
    unit,
    COUNT(*) as samples,
    AVG(metric_value) as avg_value,
    MIN(metric_value) as min_value,
    MAX(metric_value) as max_value
FROM system_metrics
WHERE recorded_at >= NOW() - INTERVAL '24 hours'
GROUP BY metric_type, unit
ORDER BY metric_type;

-- Metric trends (hourly aggregation)
SELECT 
    DATE_TRUNC('hour', recorded_at) as hour,
    metric_type,
    AVG(metric_value) as avg_value,
    MAX(metric_value) as max_value
FROM system_metrics
WHERE recorded_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', recorded_at), metric_type
ORDER BY hour DESC, metric_type;
```

### Combined Analytics

```sql
-- User engagement funnel
WITH user_events AS (
    SELECT 
        user_id,
        DATE(timestamp) as date,
        COUNT(*) FILTER (WHERE event_type = 'page_view') as page_views,
        COUNT(*) FILTER (WHERE event_type = 'contract_search') as searches,
        COUNT(*) FILTER (WHERE event_type = 'contract_analyzed') as analyses
    FROM analytics_events
    WHERE timestamp >= NOW() - INTERVAL '7 days'
    GROUP BY user_id, DATE(timestamp)
)
SELECT 
    date,
    COUNT(DISTINCT user_id) as total_users,
    COUNT(DISTINCT user_id) FILTER (WHERE page_views > 0) as viewed,
    COUNT(DISTINCT user_id) FILTER (WHERE searches > 0) as searched,
    COUNT(DISTINCT user_id) FILTER (WHERE analyses > 0) as analyzed
FROM user_events
GROUP BY date
ORDER BY date DESC;

-- Revenue per user segment
SELECT 
    u.role,
    COUNT(DISTINCT u.id) as user_count,
    COUNT(r.id) as transactions,
    SUM(r.amount) as total_revenue,
    AVG(r.amount) as avg_transaction
FROM analytics_users u
LEFT JOIN revenue_events r ON u.id::text = r.user_id
WHERE u.created_at >= NOW() - INTERVAL '90 days'
GROUP BY u.role
ORDER BY total_revenue DESC;

-- Retention cohort (simplified)
SELECT 
    DATE_TRUNC('week', first_seen) as cohort_week,
    COUNT(DISTINCT user_id) as cohort_size,
    COUNT(DISTINCT CASE 
        WHEN last_seen >= first_seen + INTERVAL '7 days' 
        THEN user_id 
    END) as retained_week_1,
    COUNT(DISTINCT CASE 
        WHEN last_seen >= first_seen + INTERVAL '14 days' 
        THEN user_id 
    END) as retained_week_2
FROM (
    SELECT 
        user_id,
        MIN(timestamp) as first_seen,
        MAX(timestamp) as last_seen
    FROM analytics_events
    WHERE user_id IS NOT NULL
    GROUP BY user_id
) user_activity
GROUP BY DATE_TRUNC('week', first_seen)
ORDER BY cohort_week DESC;
```

## Insert Examples

### Track Event

```sql
INSERT INTO analytics_events (event_type, user_id, session_id, metadata)
VALUES (
    'contract_viewed',
    'user-123',
    'session-456',
    '{"contract_id": "CNT-789", "source": "dashboard"}'::jsonb
);
```

### Create User Session

```sql
INSERT INTO user_sessions (session_id, user_id, metadata)
VALUES (
    'session-abc123',
    'user-456',
    '{"device": "desktop", "browser": "chrome"}'::jsonb
);
```

### Update Session on End

```sql
UPDATE user_sessions
SET 
    ended_at = NOW(),
    duration_seconds = EXTRACT(EPOCH FROM (NOW() - started_at))::INTEGER,
    page_views = 15,
    actions_count = 23
WHERE session_id = 'session-abc123';
```

### Record Revenue

```sql
INSERT INTO revenue_events (user_id, transaction_id, amount, product_type, subscription_tier)
VALUES (
    'user-789',
    'txn-xyz456',
    99.99,
    'subscription',
    'professional'
);
```

### Record Contract Analysis

```sql
INSERT INTO contract_analyses (contract_id, user_id, contract_type, results)
VALUES (
    'CNT-001',
    'user-123',
    'government_contract',
    '{
        "analysis_score": 85,
        "risk_level": "low",
        "compliance_status": "compliant",
        "key_findings": ["Finding 1", "Finding 2"]
    }'::jsonb
);
```

### Record System Metric

```sql
INSERT INTO system_metrics (metric_type, metric_value, unit, metadata)
VALUES (
    'api_response_time',
    245.67,
    'milliseconds',
    '{"endpoint": "/api/contracts", "method": "GET"}'::jsonb
);
```

## Useful JSONB Queries

### Query JSONB Fields

```sql
-- Extract specific field from metadata
SELECT 
    event_type,
    metadata->>'contract_id' as contract_id,
    metadata->>'source' as source
FROM analytics_events
WHERE metadata->>'source' = 'dashboard';

-- Filter by JSONB array contains
SELECT *
FROM contract_analyses
WHERE results->'key_findings' @> '["Finding 1"]'::jsonb;

-- Extract nested JSONB field
SELECT 
    contract_id,
    results->'compliance_status' as compliance,
    results->'analysis_score' as score
FROM contract_analyses
WHERE (results->>'analysis_score')::numeric > 80;
```

### Update JSONB Fields

```sql
-- Add/update field in JSONB
UPDATE analytics_events
SET metadata = metadata || '{"updated": true}'::jsonb
WHERE event_type = 'contract_viewed';

-- Remove field from JSONB
UPDATE analytics_events
SET metadata = metadata - 'temporary_field'
WHERE id = 'some-uuid';
```

## Performance Tips

1. **Use indexes wisely**: The schema includes GIN indexes for JSONB columns
2. **Filter on indexed columns**: Use `event_type`, `user_id`, and timestamp fields in WHERE clauses
3. **Limit result sets**: Always use LIMIT for large tables
4. **Use views for complex queries**: Pre-defined views are optimized
5. **Partition large tables**: Consider time-based partitioning for `analytics_events`
6. **Regular VACUUM**: Run `VACUUM ANALYZE` periodically on large tables

## Maintenance Queries

```sql
-- Table sizes
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Dead tuples (needs cleanup)
SELECT 
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_percentage
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Data Cleanup

```sql
-- Archive old events (example: move to archive table)
CREATE TABLE IF NOT EXISTS analytics_events_archive (LIKE analytics_events INCLUDING ALL);

INSERT INTO analytics_events_archive
SELECT * FROM analytics_events
WHERE timestamp < NOW() - INTERVAL '1 year';

DELETE FROM analytics_events
WHERE timestamp < NOW() - INTERVAL '1 year';

-- Delete old metrics
DELETE FROM system_metrics
WHERE recorded_at < NOW() - INTERVAL '90 days';
```
