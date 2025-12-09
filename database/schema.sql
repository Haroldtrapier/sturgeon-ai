-- Sturgeon AI Database Schema
-- Run this migration in your Supabase SQL editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- GRANTS TABLES
-- ============================================================================

CREATE TABLE grants (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  external_id VARCHAR(255) UNIQUE NOT NULL,
  title TEXT NOT NULL,
  agency VARCHAR(255) NOT NULL,
  amount VARCHAR(100),
  deadline TIMESTAMP WITH TIME ZONE,
  category VARCHAR(100),
  description TEXT,
  eligibility JSONB DEFAULT '[]',
  requirements JSONB DEFAULT '[]',
  source VARCHAR(50) NOT NULL, -- 'grants.gov', 'usaspending.gov', 'sam.gov'
  match_score INTEGER DEFAULT 0,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_grants_agency ON grants(agency);
CREATE INDEX idx_grants_deadline ON grants(deadline);
CREATE INDEX idx_grants_category ON grants(category);
CREATE INDEX idx_grants_source ON grants(source);

CREATE TABLE saved_grants (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  grant_id UUID REFERENCES grants(id) ON DELETE CASCADE,
  notes TEXT,
  saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, grant_id)
);

CREATE INDEX idx_saved_grants_user ON saved_grants(user_id);

-- ============================================================================
-- OPPORTUNITIES TABLES
-- ============================================================================

CREATE TABLE opportunities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  external_id VARCHAR(255) UNIQUE,
  title TEXT NOT NULL,
  agency VARCHAR(255),
  type VARCHAR(100), -- 'grant', 'contract', 'cooperative_agreement'
  amount VARCHAR(100),
  deadline TIMESTAMP WITH TIME ZONE,
  status VARCHAR(50) DEFAULT 'active', -- 'active', 'closed', 'archived'
  description TEXT,
  requirements JSONB DEFAULT '[]',
  attachments JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_opportunities_agency ON opportunities(agency);
CREATE INDEX idx_opportunities_type ON opportunities(type);
CREATE INDEX idx_opportunities_deadline ON opportunities(deadline);
CREATE INDEX idx_opportunities_status ON opportunities(status);

CREATE TABLE saved_opportunities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  opportunity_id UUID REFERENCES opportunities(id) ON DELETE CASCADE,
  notes TEXT,
  saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, opportunity_id)
);

-- ============================================================================
-- PROPOSALS TABLES
-- ============================================================================

CREATE TABLE proposals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  opportunity_id UUID REFERENCES opportunities(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'in-progress', 'review', 'submitted', 'approved', 'rejected'
  total_word_count INTEGER DEFAULT 0,
  team_id UUID,
  submitted_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_proposals_user ON proposals(user_id);
CREATE INDEX idx_proposals_status ON proposals(status);
CREATE INDEX idx_proposals_team ON proposals(team_id);

CREATE TABLE proposal_sections (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  proposal_id UUID REFERENCES proposals(id) ON DELETE CASCADE,
  section_id VARCHAR(100) NOT NULL,
  title TEXT NOT NULL,
  content TEXT DEFAULT '',
  word_count INTEGER DEFAULT 0,
  required BOOLEAN DEFAULT false,
  ai_generated BOOLEAN DEFAULT false,
  order_index INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(proposal_id, section_id)
);

CREATE INDEX idx_proposal_sections_proposal ON proposal_sections(proposal_id);

-- ============================================================================
-- DOCUMENTS TABLES
-- ============================================================================

CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  original_name VARCHAR(255) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  file_size BIGINT NOT NULL,
  s3_key TEXT NOT NULL,
  s3_url TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'uploaded', -- 'uploaded', 'processing', 'completed', 'failed'
  parsed_content TEXT,
  extracted_data JSONB DEFAULT '{}',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_documents_user ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(status);

-- ============================================================================
-- COMPLIANCE TABLES
-- ============================================================================

CREATE TABLE compliance_reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  proposal_id UUID REFERENCES proposals(id) ON DELETE CASCADE,
  regulation_type VARCHAR(50) NOT NULL, -- 'FAR', 'DFARS', 'FISMA', 'CMMC', 'ALL'
  overall_status VARCHAR(50) NOT NULL, -- 'compliant', 'non-compliant', 'needs-review'
  score INTEGER NOT NULL,
  checks JSONB NOT NULL DEFAULT '[]',
  recommendations JSONB DEFAULT '[]',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_compliance_document ON compliance_reports(document_id);
CREATE INDEX idx_compliance_proposal ON compliance_reports(proposal_id);
CREATE INDEX idx_compliance_regulation ON compliance_reports(regulation_type);

-- ============================================================================
-- TEAM TABLES
-- ============================================================================

CREATE TABLE teams (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  owner_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE team_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  role VARCHAR(50) NOT NULL DEFAULT 'viewer', -- 'owner', 'admin', 'editor', 'viewer'
  status VARCHAR(50) DEFAULT 'active', -- 'invited', 'active', 'inactive'
  invited_by UUID REFERENCES auth.users(id),
  joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(team_id, user_id)
);

CREATE INDEX idx_team_members_team ON team_members(team_id);
CREATE INDEX idx_team_members_user ON team_members(user_id);

-- ============================================================================
-- NOTIFICATIONS TABLES
-- ============================================================================

CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL, -- 'deadline', 'update', 'team', 'system'
  priority VARCHAR(20) DEFAULT 'medium', -- 'high', 'medium', 'low'
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  action_url TEXT,
  is_read BOOLEAN DEFAULT false,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_notifications_type ON notifications(type);

-- ============================================================================
-- ANALYTICS TABLES
-- ============================================================================

CREATE TABLE analytics_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  event_type VARCHAR(100) NOT NULL,
  event_data JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_analytics_user ON analytics_events(user_id);
CREATE INDEX idx_analytics_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_created ON analytics_events(created_at);

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Auto update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers
CREATE TRIGGER update_grants_updated_at BEFORE UPDATE ON grants
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_proposals_updated_at BEFORE UPDATE ON proposals
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

ALTER TABLE saved_grants ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE proposal_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Saved grants policies
CREATE POLICY "Users can view their own saved grants"
  ON saved_grants FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own saved grants"
  ON saved_grants FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own saved grants"
  ON saved_grants FOR DELETE
  USING (auth.uid() = user_id);

-- Proposals policies
CREATE POLICY "Users can view their own proposals"
  ON proposals FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own proposals"
  ON proposals FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own proposals"
  ON proposals FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own proposals"
  ON proposals FOR DELETE
  USING (auth.uid() = user_id);

-- Documents policies
CREATE POLICY "Users can view their own documents"
  ON documents FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own documents"
  ON documents FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own documents"
  ON documents FOR UPDATE
  USING (auth.uid() = user_id);

-- Notifications policies
CREATE POLICY "Users can view their own notifications"
  ON notifications FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own notifications"
  ON notifications FOR UPDATE
  USING (auth.uid() = user_id);

-- ============================================================================
-- INITIAL DATA / SEED (Optional)
-- ============================================================================

-- Sample notification for testing
-- INSERT INTO notifications (user_id, type, priority, title, message)
-- VALUES (
--   auth.uid(),
--   'system',
--   'medium',
--   'Welcome to Sturgeon AI',
--   'Your account has been set up successfully. Start exploring grants and opportunities!'
-- );
