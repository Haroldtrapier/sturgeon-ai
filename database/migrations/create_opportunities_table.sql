-- Create opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL,
    agency VARCHAR(255),
    source VARCHAR(50) NOT NULL,
    external_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'watchlist',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT opportunities_user_external_unique UNIQUE(user_id, external_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_opportunities_user_id ON opportunities(user_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opportunities_source ON opportunities(source);
CREATE INDEX IF NOT EXISTS idx_opportunities_created_at ON opportunities(created_at DESC);

-- Enable Row Level Security
ALTER TABLE opportunities ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own opportunities" ON opportunities
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own opportunities" ON opportunities
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own opportunities" ON opportunities
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own opportunities" ON opportunities
    FOR DELETE USING (auth.uid() = user_id);

-- Auto-update timestamp function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to update timestamp
CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE
    ON opportunities FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE opportunities IS 'Stores government contract opportunities saved by users';
