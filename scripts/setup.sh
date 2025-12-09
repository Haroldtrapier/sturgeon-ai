#!/bin/bash
# Sturgeon AI - Automated Setup Script

set -e

echo "🚀 Sturgeon AI Setup Starting..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Node.js
echo "${BLUE}[1/7]${NC} Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "${RED}❌ Node.js is not installed. Please install Node.js 18+ first.${NC}"
    exit 1
fi
echo "${GREEN}✅ Node.js $(node --version) found${NC}"
echo ""

# Step 2: Install dependencies
echo "${BLUE}[2/7]${NC} Installing dependencies..."
npm install @supabase/supabase-js openai axios formidable pdf-parse mammoth uuid
npm install -D @types/formidable @types/uuid
echo "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Step 3: Setup environment
echo "${BLUE}[3/7]${NC} Setting up environment variables..."
if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo "${GREEN}✅ Created .env.local from template${NC}"
    echo "${RED}⚠️  IMPORTANT: Edit .env.local and add your API keys!${NC}"
else
    echo "${GREEN}✅ .env.local already exists${NC}"
fi
echo ""

# Step 4: Check Supabase connection
echo "${BLUE}[4/7]${NC} Checking Supabase configuration..."
if grep -q "your_supabase_project_url" .env.local; then
    echo "${RED}⚠️  Supabase URL not configured. Please update .env.local${NC}"
else
    echo "${GREEN}✅ Supabase URL configured${NC}"
fi
echo ""

# Step 5: Database setup instructions
echo "${BLUE}[5/7]${NC} Database setup..."
echo "📋 To set up your database:"
echo "   1. Go to your Supabase dashboard"
echo "   2. Navigate to SQL Editor"
echo "   3. Copy contents of database/schema.sql"
echo "   4. Paste and execute in SQL Editor"
echo ""
read -p "Have you completed the database setup? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "${GREEN}✅ Database setup confirmed${NC}"
else
    echo "${RED}⚠️  Remember to run database migration before starting!${NC}"
fi
echo ""

# Step 6: Supabase Storage setup
echo "${BLUE}[6/7]${NC} Supabase Storage setup..."
echo "📦 To set up document storage:"
echo "   1. Go to Supabase Dashboard → Storage"
echo "   2. Create a new bucket named 'documents'"
echo "   3. Set bucket to public or configure RLS policies"
echo ""
read -p "Have you created the storage bucket? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "${GREEN}✅ Storage bucket confirmed${NC}"
else
    echo "${RED}⚠️  Remember to create storage bucket!${NC}"
fi
echo ""

# Step 7: Final checks
echo "${BLUE}[7/7]${NC} Running final checks..."
echo ""

echo "📝 Summary:"
echo "   ${GREEN}✅ Dependencies installed${NC}"
echo "   ${GREEN}✅ Environment template created${NC}"

if grep -q "your_supabase_project_url" .env.local || grep -q "your_openai_api_key" .env.local; then
    echo "   ${RED}❌ API keys need to be configured${NC}"
else
    echo "   ${GREEN}✅ API keys configured${NC}"
fi

echo ""
echo "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. ${BLUE}Edit .env.local${NC} and add your API keys"
echo "  2. ${BLUE}Run database migration${NC} (database/schema.sql)"
echo "  3. ${BLUE}Create Supabase storage bucket${NC} named 'documents'"
echo "  4. ${BLUE}Start dev server:${NC} npm run dev"
echo "  5. ${BLUE}Test API:${NC} curl -X POST http://localhost:3000/api/grants/search -H "Content-Type: application/json" -d '{"keyword":"research"}'"
echo ""
echo "📚 Documentation:"
echo "  - Frontend: PHASE1_SETUP.md"
echo "  - Backend: BACKEND_README.md"
echo "  - Full guide: COMPLETE_SETUP_GUIDE.md"
echo ""
