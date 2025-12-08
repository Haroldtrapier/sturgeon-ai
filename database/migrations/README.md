# Database Migrations

This directory contains SQL migration files for the Sturgeon AI platform.

## Available Migrations

### Core Tables
- `create_profiles_table.sql` - User profile and company information for government contracting
- `create_opportunities_table.sql` - Government contract opportunities tracking

### Analytics Dashboard
- `create_analytics_dashboard.sql` - Comprehensive analytics and monitoring schema

## Analytics Dashboard Schema

The `create_analytics_dashboard.sql` migration provides a complete analytics infrastructure including:

### Tables
1. **analytics_events** - Track user events and interactions
2. **analytics_users** - Enhanced user information with activity tracking (separate from core users table)
3. **contract_analyses** - Store contract analysis results
4. **user_sessions** - Track user session data
5. **revenue_events** - Financial transaction tracking
6. **system_metrics** - System performance monitoring

### Views
- **daily_active_users** - Daily active user metrics
- **revenue_summary** - Revenue analytics by date, product, and tier
- **contract_analysis_summary** - Contract analysis statistics

### Security
- Row Level Security (RLS) enabled on all tables
- Service role policies for backend access
- Secure data isolation

## Usage

### Running Migrations

These migrations should be run in your Supabase SQL Editor in the following order:

1. Run core table migrations first:
   ```sql
   -- Run create_profiles_table.sql
   -- Run create_opportunities_table.sql
   ```

2. Run analytics dashboard migration:
   ```sql
   -- Run create_analytics_dashboard.sql
   ```

### Important Notes

- All migrations use `CREATE TABLE IF NOT EXISTS` to prevent errors on re-runs
- Indexes are created with `IF NOT EXISTS` where supported
- RLS policies are created to ensure data security
- Sample data is included for testing purposes

## Sample Data

The analytics dashboard migration includes sample users:
- `admin@trapier.com` - Harold Trapier (Admin)
- `demo@government.gov` - Demo User (Analyst)

These can be used for testing the analytics dashboard functionality.

## Indexes

All tables include optimized indexes for:
- Primary key lookups
- User-based queries
- Time-series analysis
- JSONB field searches (GIN indexes)

## Maintenance

### Updating Timestamps
Automatic timestamp updates are handled by triggers on:
- `analytics_users.updated_at`
- `contract_analyses.updated_at`

These use the `update_updated_at_column()` function (defined in create_opportunities_table.sql).

### Important Notes
- The `analytics_users` table is separate from the core `users` table to avoid conflicts
- All UUID fields use `gen_random_uuid()` for consistency with the rest of the schema
- All timestamps use `CURRENT_TIMESTAMP` for consistency
- All indexes use `IF NOT EXISTS` to allow safe re-running of migrations
- User ID fields use UUID type to match the core schema and enable proper foreign key relationships
