# 🐟 Sturgeon AI - Government Contracting Platform

AI-powered government contracting and grant management platform with integrated SAM.gov and Grants.gov search capabilities.

## 🚀 Features

### ✅ Live API Endpoints
- **SAM.gov Integration** - Search federal contracts
- **Grants.gov Integration** - Find grant opportunities
- **AI Contract Analysis** - Intelligent requirement analysis
- **AI Proposal Generation** - Automated proposal writing
- **Opportunity Matching** - Smart contract-to-company matching
- **Document Management** - Upload and manage documents
- **Analytics Dashboard** - Performance metrics and insights

### ✅ Frontend Pages
- **Login Page** - Secure authentication
- **Dashboard** - Overview with key metrics
- **Opportunities** - Search and browse contracts/grants
- **Proposals** - AI-powered proposal builder
- **Analytics** - Performance tracking and charts

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 (React 18)
- TypeScript
- Tailwind CSS
- Recharts (Analytics)
- Axios (API calls)

**Backend:**
- FastAPI (Python)
- OpenAI GPT-4 (AI features)
- SAM.gov API
- Grants.gov API
- Supabase (Database)

## 📦 Installation

### Frontend Setup
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

### Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run API server
uvicorn main:app --reload
```

## 🔧 Environment Variables

Create `.env.local` in root:
```
NEXT_PUBLIC_API_URL=https://sturgeon-ai-prod.vercel.app
```

Create `backend/.env`:
```
OPENAI_API_KEY=your_openai_key
SAM_GOV_API_KEY=your_sam_gov_key
GRANTS_GOV_API_KEY=your_grants_gov_key
```

## 🚀 Deployment

### Frontend (Vercel)
```bash
vercel --prod
```

### Backend (Vercel)
```bash
cd backend
vercel --prod
```

### Environment Variables in Vercel
Add these in your Vercel project settings:
- `NEXT_PUBLIC_API_URL`
- `OPENAI_API_KEY`
- `SAM_GOV_API_KEY`
- `GRANTS_GOV_API_KEY`

## 📊 Database Schema

15 production tables in Supabase:
- users, organizations, team_members
- opportunities, contracts, grants
- proposals, submissions
- compliance_checks, compliance_docs
- notifications, audit_logs
- ai_interactions, research_notes, sbir_projects

## 🔗 API Documentation

Visit `/docs` on your backend URL for interactive API documentation (FastAPI auto-generated).

### Key Endpoints:
- `GET /health` - Health check
- `GET /api/opportunities/search` - Search contracts
- `GET /api/grants/search` - Search grants
- `POST /api/ai/analyze-contract` - Analyze requirements
- `POST /api/ai/generate-proposal` - Generate proposal
- `POST /api/ai/match-opportunities` - Match opportunities
- `GET /api/analytics/dashboard` - Get analytics

## 🎯 Usage

1. **Login** - Access the platform at `/login`
2. **Dashboard** - View your metrics and quick actions
3. **Find Opportunities** - Search SAM.gov and Grants.gov
4. **Create Proposals** - Use AI to generate winning proposals
5. **Track Performance** - Monitor your analytics

## 🤝 Contributing

This is a production government contracting platform. For contributions or issues, please contact the development team.

## 📄 License

MIT License - see LICENSE file

## 🔒 Security

- FedRAMP compliant infrastructure
- FISMA security controls
- Data encryption at rest and in transit
- Regular security audits

---

**Built with ❤️ for government contractors**

For questions or support, visit our documentation or contact support.
