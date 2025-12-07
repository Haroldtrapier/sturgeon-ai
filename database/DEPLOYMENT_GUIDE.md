# Analytics Dashboard Schema Deployment Guide

This guide provides step-by-step instructions for deploying the analytics dashboard database schema to Supabase.

## Prerequisites

- Supabase project created and accessible
- Access to Supabase SQL Editor or Supabase CLI
- Database connection URL (if using CLI)

## Deployment Options

### Option 1: Supabase Dashboard (Recommended)

This is the easiest method for deploying the analytics schema.

1. **Login to Supabase Dashboard**
   - Navigate to [https://app.supabase.com](https://app.supabase.com)
   - Select your project

2. **Open SQL Editor**
   - Click on "SQL Editor" in the left sidebar
   - Click "New query"

3. **Run the Analytics Schema**
   - Copy the entire contents of `database/migrations/create_analytics_schema.sql`
   - Paste into the SQL Editor
   - Click "Run" or press `Ctrl+Enter`

4. **Verify Success**
   - Check for success message in the SQL Editor
   - Navigate to "Table Editor" to see the new tables
   - Tables should include: `analytics_events`, `analytics_users`, `contract_analyses`, `user_sessions`, `revenue_events`, `system_metrics`

### Option 2: Supabase CLI

For automated deployments or CI/CD pipelines.

```bash
# Install Supabase CLI (if not already installed)
npm install -g supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref your-project-ref

# Run the migration
supabase db push

# Or run a specific migration file
psql $DATABASE_URL -f database/migrations/create_analytics_schema.sql
```

### Option 3: Direct PostgreSQL Connection

For advanced users with direct database access.

**⚠️ SECURITY WARNING**: Never include passwords directly in commands or scripts. Always use environment variables or secure credential management.

```bash
# Recommended: Using environment variable (secure)
export DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
psql $DATABASE_URL -f database/migrations/create_analytics_schema.sql

# Or use a .pgpass file for secure credential storage
# Create ~/.pgpass with: hostname:port:database:username:password
# Then: chmod 600 ~/.pgpass
psql -h db.[PROJECT-REF].supabase.co -U postgres -d postgres \
  -f database/migrations/create_analytics_schema.sql

# NOT RECOMMENDED: Direct password in command (shown for reference only)
# psql "postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres" \
#   -f database/migrations/create_analytics_schema.sql
```

## Verification Steps

After deployment, verify the schema was created correctly:

### 1. Check Tables

```sql
-- List all analytics tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND (table_name LIKE '%analytics%' 
    OR table_name IN ('contract_analyses', 'user_sessions', 'revenue_events', 'system_metrics'))
ORDER BY table_name;
```

Expected tables:
- `analytics_events`
- `analytics_users`
- `contract_analyses`
- `user_sessions`
- `revenue_events`
- `system_metrics`

### 2. Check Views

```sql
-- List all views
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Expected views:
- `daily_active_users`
- `revenue_summary`
- `contract_analysis_summary`

### 3. Check Indexes

```sql
-- List indexes for analytics tables
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND (tablename LIKE '%analytics%' 
    OR tablename IN ('contract_analyses', 'user_sessions', 'revenue_events', 'system_metrics'))
ORDER BY tablename, indexname;
```

### 4. Check RLS Policies

```sql
-- List Row Level Security policies
SELECT 
    schemaname,
    tablename,
    policyname,
    roles,
    cmd,
    qual
FROM pg_policies
WHERE schemaname = 'public'
  AND (tablename LIKE '%analytics%' 
    OR tablename IN ('contract_analyses', 'user_sessions', 'revenue_events', 'system_metrics'))
ORDER BY tablename, policyname;
```

### 5. Test Sample Data

```sql
-- Check sample users were inserted
SELECT email, full_name, company, role 
FROM analytics_users
WHERE email IN ('admin@trapier.com', 'demo@government.gov');
```

Expected results: 2 rows with the test users.

## Post-Deployment Configuration

### 1. Set Up Service Role Access

The schema includes RLS policies that grant full access to the `service_role`. Ensure your backend application uses the service role key:

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY // Use service role for backend operations
)
```

### 2. Configure Environment Variables

Add these to your `.env` or `.env.local`:

```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### 3. Backend Integration

Example code to track analytics events:

```javascript
// Track user event
async function trackEvent(eventType, userId, sessionId, metadata = {}) {
  const { data, error } = await supabase
    .from('analytics_events')
    .insert({
      event_type: eventType,
      user_id: userId,
      session_id: sessionId,
      metadata: metadata,
      timestamp: new Date().toISOString()
    })
  
  if (error) console.error('Error tracking event:', error)
  return data
}

// Track revenue
async function trackRevenue(userId, transactionId, amount, productType, subscriptionTier) {
  const { data, error } = await supabase
    .from('revenue_events')
    .insert({
      user_id: userId,
      transaction_id: transactionId,
      amount: amount,
      product_type: productType,
      subscription_tier: subscriptionTier
    })
  
  if (error) console.error('Error tracking revenue:', error)
  return data
}
```

## Troubleshooting

### Issue: "extension 'uuid-ossp' does not exist"

**Solution**: Supabase projects should have this extension enabled by default. If not, run:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Issue: "policy already exists"

**Solution**: This can happen if re-running the migration. Drop existing policies first:

```sql
DROP POLICY IF EXISTS "Service role has full access to analytics_events" ON analytics_events;
-- Repeat for other tables
```

Then re-run the migration.

### Issue: "relation already exists"

**Solution**: Tables already exist. Either:
1. Drop the tables first (⚠️ **WARNING: This deletes all data**)
   ```sql
   DROP TABLE IF EXISTS analytics_events CASCADE;
   -- Repeat for other tables
   ```
2. Or modify the migration to use `CREATE TABLE IF NOT EXISTS` (already included)

### Issue: RLS blocking queries

**Solution**: Ensure you're using the service role key for backend operations:
- Check that `SUPABASE_SERVICE_ROLE_KEY` is set correctly
- Verify you're creating the client with the service role key
- RLS policies allow full access to service_role

### Issue: Views not showing data

**Solution**: 
1. Verify data exists in the underlying tables
2. Check view definitions match your table structure
3. Re-create views if needed:
   ```sql
   DROP VIEW IF EXISTS daily_active_users;
   -- Then run the CREATE VIEW statement again
   ```

## Monitoring and Maintenance

### Monitor Table Growth

```sql
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
  AND (tablename LIKE '%analytics%' 
    OR tablename IN ('contract_analyses', 'user_sessions', 'revenue_events', 'system_metrics'))
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Set Up Regular Backups

Use Supabase's automatic backup feature or set up custom backups:

```bash
# Daily backup script
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Optimize Performance

Monitor slow queries and add indexes as needed:

```sql
-- Find slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
WHERE query LIKE '%analytics%'
ORDER BY mean_time DESC
LIMIT 10;
```

## Rollback Procedure

If you need to remove the analytics schema:

```sql
-- Drop views first
DROP VIEW IF EXISTS daily_active_users CASCADE;
DROP VIEW IF EXISTS revenue_summary CASCADE;
DROP VIEW IF EXISTS contract_analysis_summary CASCADE;

-- Drop tables (⚠️ WARNING: This deletes all data)
DROP TABLE IF EXISTS analytics_events CASCADE;
DROP TABLE IF EXISTS analytics_users CASCADE;
DROP TABLE IF EXISTS contract_analyses CASCADE;
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS revenue_events CASCADE;
DROP TABLE IF EXISTS system_metrics CASCADE;

-- Drop function
DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;
```

## Support

For additional help:
- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- Project repository issues

## Next Steps

After successful deployment:
1. ✅ Verify all tables and views are created
2. ✅ Test sample queries against views
3. ✅ Integrate analytics tracking in your application
4. ✅ Set up monitoring and alerting
5. ✅ Configure regular backups
6. ✅ Document custom queries for your analytics dashboard
