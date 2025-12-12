-- Sturgeon AI Analytics Dashboard - Database Schema
-- Run this in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Analytics Events Table
-- Note: 'timestamp' represents the actual event time (can be set by client)
-- 'created_at' represents when the record was inserted into the database
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(50) NOT NULL,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    metadata JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_analytics_events_event_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_timestamp ON analytics_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_events_metadata ON analytics_events USING GIN(metadata);

-- Users Table (Enhanced for Analytics)
CREATE TABLE IF NOT EXISTS analytics_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    company VARCHAR(255),
    role VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT true
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_analytics_users_email ON analytics_users(email);
CREATE INDEX IF NOT EXISTS idx_analytics_users_created_at ON analytics_users(created_at DESC);

-- Contract Analyses Table
CREATE TABLE IF NOT EXISTS contract_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    contract_type VARCHAR(100),
    results JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'completed',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_contract_analyses_contract_id ON contract_analyses(contract_id);
CREATE INDEX IF NOT EXISTS idx_contract_analyses_user_id ON contract_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_contract_analyses_created_at ON contract_analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_contract_analyses_results ON contract_analyses USING GIN(results);

-- User Sessions Table
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255),
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    page_views INTEGER DEFAULT 0,
    actions_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_sessions_session_id ON user_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_started_at ON user_sessions(started_at DESC);

-- Revenue Tracking Table
CREATE TABLE IF NOT EXISTS revenue_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL,
    transaction_id VARCHAR(255) UNIQUE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    product_type VARCHAR(100),
    subscription_tier VARCHAR(50),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_revenue_events_transaction_id ON revenue_events(transaction_id);
CREATE INDEX IF NOT EXISTS idx_revenue_events_user_id ON revenue_events(user_id);
CREATE INDEX IF NOT EXISTS idx_revenue_events_created_at ON revenue_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_revenue_events_amount ON revenue_events(amount);

-- System Metrics Table (for monitoring)
CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_type VARCHAR(50) NOT NULL,
    metric_value DECIMAL(12, 4) NOT NULL,
    unit VARCHAR(20),
    metadata JSONB DEFAULT '{}'::jsonb,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_system_metrics_type ON system_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_system_metrics_recorded_at ON system_metrics(recorded_at DESC);

-- Create view for daily active users
CREATE OR REPLACE VIEW daily_active_users AS
SELECT 
    DATE(timestamp) as date,
    COUNT(DISTINCT user_id) as active_users
FROM analytics_events
WHERE user_id IS NOT NULL
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Create view for revenue summary
CREATE OR REPLACE VIEW revenue_summary AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as transaction_count,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_transaction_value,
    product_type,
    subscription_tier
FROM revenue_events
GROUP BY DATE(created_at), product_type, subscription_tier
ORDER BY date DESC;

-- Create view for contract analysis summary
CREATE OR REPLACE VIEW contract_analysis_summary AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_analyses,
    user_id,
    JSONB_AGG(results->'analysis_score') FILTER (WHERE results->'analysis_score' IS NOT NULL) as scores
FROM contract_analyses
GROUP BY DATE(created_at), user_id
ORDER BY date DESC;

-- Enable Row Level Security (RLS)
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE contract_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE revenue_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_metrics ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (service role has full access)
CREATE POLICY "Service role has full access to analytics_events" 
ON analytics_events FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

CREATE POLICY "Service role has full access to analytics_users" 
ON analytics_users FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

CREATE POLICY "Service role has full access to contract_analyses" 
ON contract_analyses FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

CREATE POLICY "Service role has full access to user_sessions" 
ON user_sessions FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

CREATE POLICY "Service role has full access to revenue_events" 
ON revenue_events FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

CREATE POLICY "Service role has full access to system_metrics" 
ON system_metrics FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

-- Insert sample data for testing
INSERT INTO analytics_users (email, full_name, company, role) VALUES
('admin@trapier.com', 'Harold Trapier', 'Trapier Management LLC', 'Admin'),
('demo@government.gov', 'Demo User', 'Department of Defense', 'Analyst')
ON CONFLICT (email) DO NOTHING;

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_analytics_users_updated_at BEFORE UPDATE ON analytics_users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contract_analyses_updated_at BEFORE UPDATE ON contract_analyses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE analytics_events IS 'Stores all user interaction events for analytics tracking';
COMMENT ON TABLE analytics_users IS 'Extended user information for analytics dashboard';
COMMENT ON TABLE contract_analyses IS 'Tracks contract analysis results and metrics';
COMMENT ON TABLE user_sessions IS 'User session tracking for engagement analytics';
COMMENT ON TABLE revenue_events IS 'Revenue and transaction tracking for business metrics';
COMMENT ON TABLE system_metrics IS 'System performance and health monitoring metrics';
