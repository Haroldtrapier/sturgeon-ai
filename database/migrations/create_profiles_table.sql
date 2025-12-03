-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    company_name VARCHAR(255) NOT NULL,
    naics_codes TEXT[] DEFAULT ARRAY[]::TEXT[],
    psc_codes TEXT[] DEFAULT ARRAY[]::TEXT[],
    cage_code VARCHAR(5),
    duns VARCHAR(9),
    capabilities_summary TEXT,
    certifications TEXT[] DEFAULT ARRAY[]::TEXT[],
    phone VARCHAR(20),
    website VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT profiles_user_id_unique UNIQUE(user_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_company_name ON profiles(company_name);
CREATE INDEX IF NOT EXISTS idx_profiles_cage_code ON profiles(cage_code);
CREATE INDEX IF NOT EXISTS idx_profiles_naics_codes ON profiles USING GIN(naics_codes);
CREATE INDEX IF NOT EXISTS idx_profiles_psc_codes ON profiles USING GIN(psc_codes);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own profile" ON profiles
    FOR DELETE USING (auth.uid() = user_id);

-- Auto-update timestamp function
CREATE OR REPLACE FUNCTION update_profiles_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to update timestamp
CREATE TRIGGER update_profiles_timestamp BEFORE UPDATE
    ON profiles FOR EACH ROW
    EXECUTE FUNCTION update_profiles_updated_at();

COMMENT ON TABLE profiles IS 'Stores company profile information for government contracting';
COMMENT ON COLUMN profiles.naics_codes IS 'North American Industry Classification System codes';
COMMENT ON COLUMN profiles.psc_codes IS 'Product Service Codes';
COMMENT ON COLUMN profiles.cage_code IS 'Commercial and Government Entity Code';
COMMENT ON COLUMN profiles.duns IS 'Data Universal Numbering System (legacy)';
