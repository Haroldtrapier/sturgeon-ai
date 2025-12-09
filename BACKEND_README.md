# Sturgeon AI Backend - Implementation Guide

## 🎯 Overview

Complete backend infrastructure for Sturgeon AI including:
- **10 API Routes** (Grants, AI, Compliance, Proposals, Documents)
- **Comprehensive Database Schema** (Supabase/PostgreSQL)
- **Utility Functions** (Auth, Document Parsing, Supabase Client)
- **Environment Configuration**

---

## 📁 File Structure

```
sturgeon-ai/
├── database/
│   └── schema.sql              # Complete database schema with RLS
├── pages/api/
│   ├── grants/
│   │   ├── search.ts          # Search grants with filters
│   │   ├── [id]/save.ts       # Save grant for user
│   │   └── sync/
│   │       └── grants-gov.ts  # Sync from Grants.gov
│   ├── ai/
│   │   ├── generate/
│   │   │   └── proposal.ts    # AI proposal generation
│   │   └── analyze/
│   │       └── contract.ts    # AI contract analysis
│   ├── compliance/
│   │   └── check.ts           # Compliance checking
│   ├── proposals/
│   │   ├── index.ts           # List/create proposals
│   │   └── [id].ts            # Update/delete proposal
│   └── documents/
│       └── upload.ts          # Document upload & parsing
├── lib/
│   ├── supabase.ts            # Supabase client
│   ├── documentParser.ts      # Document parsing utilities
│   └── authMiddleware.ts      # Auth middleware
└── .env.example               # Environment variables template
```

---

## 🚀 Setup Instructions

### 1. Database Setup

**Run the migration in Supabase SQL Editor:**

```bash
# Copy schema.sql content and paste into Supabase SQL Editor
# Or use psql:
psql YOUR_DATABASE_URL -f database/schema.sql
```

This creates:
- 12 tables (grants, proposals, documents, compliance, teams, etc.)
- Indexes for performance
- Row Level Security (RLS) policies
- Auto-update triggers

### 2. Environment Variables

```bash
# Copy environment template
cp .env.example .env.local

# Fill in your API keys (see .env.example for all variables)
```

**Required immediately:**
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_KEY`
- `OPENAI_API_KEY`

**Optional (can add later):**
- `GRANTS_GOV_API_KEY` (for grants sync)
- `USA_SPENDING_API_KEY` (for spending data)

### 3. Install Dependencies

```bash
npm install @supabase/supabase-js openai axios formidable pdf-parse mammoth uuid
npm install -D @types/formidable @types/uuid
```

### 4. Test API Routes

```bash
# Start development server
npm run dev

# Test grants search
curl -X POST http://localhost:3000/api/grants/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "research"}'

# Test AI proposal generation (requires auth)
curl -X POST http://localhost:3000/api/ai/generate/proposal \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"sectionId": "executive_summary", "context": {}}'
```

---

## 📊 Database Tables Overview

### Core Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `grants` | Grant opportunities | title, agency, amount, deadline |
| `opportunities` | All opportunities | type, status, requirements |
| `proposals` | User proposals | title, status, word_count |
| `proposal_sections` | Proposal sections | content, ai_generated |
| `documents` | Uploaded documents | s3_key, parsed_content |
| `compliance_reports` | Compliance checks | score, checks, status |
| `teams` | Team workspaces | name, owner_id |
| `team_members` | Team membership | role, status |
| `notifications` | User notifications | type, priority, is_read |

### Security

- **Row Level Security (RLS)** enabled on all user-specific tables
- **Policies** ensure users can only access their own data
- **Service role key** used for admin operations in API routes

---

## 🔌 API Endpoints

### Grants API

#### `POST /api/grants/search`
Search grants with filters.

**Request:**
```json
{
  "keyword": "research",
  "agency": "NSF",
  "category": "research",
  "minAmount": "50000",
  "maxAmount": "500000",
  "deadline": "2024-12-31"
}
```

**Response:**
```json
{
  "grants": [
    {
      "id": "uuid",
      "title": "Research Grant",
      "agency": "NSF",
      "amount": "$250,000",
      "deadline": "2024-06-30T00:00:00Z"
    }
  ]
}
```

#### `POST /api/grants/[id]/save`
Save a grant for the authenticated user.

**Headers:** `Authorization: Bearer TOKEN`

**Request:**
```json
{
  "notes": "Interesting opportunity for our team"
}
```

#### `POST /api/grants/sync/grants-gov`
Sync grants from Grants.gov (admin operation).

**Response:**
```json
{
  "synced": 95,
  "failed": 5,
  "total": 100
}
```

### AI API

#### `POST /api/ai/generate/proposal`
Generate proposal section content using AI.

**Headers:** `Authorization: Bearer TOKEN`

**Request:**
```json
{
  "sectionId": "executive_summary",
  "context": {
    "opportunityId": "opp_123",
    "requirements": ["Must address X", "Must include Y"]
  }
}
```

**Response:**
```json
{
  "content": "Generated proposal section content..."
}
```

#### `POST /api/ai/analyze/contract`
Analyze contract text using AI.

**Request:**
```json
{
  "text": "Full contract text..."
}
```

**Response:**
```json
{
  "complexity": "high",
  "keyRequirements": ["Requirement 1", "Requirement 2"],
  "deadlines": [{"item": "Proposal due", "date": "2024-06-15"}],
  "risks": [{"level": "high", "description": "Risk description"}],
  "complianceIssues": ["Issue 1"],
  "recommendations": ["Recommendation 1"]
}
```

### Compliance API

#### `POST /api/compliance/check`
Run compliance check on document or proposal.

**Request:**
```json
{
  "documentId": "doc_uuid",
  "regulationType": "FAR"
}
```

**Response:**
```json
{
  "overallStatus": "compliant",
  "score": 85,
  "checks": [
    {
      "id": "far_1",
      "category": "Contract Formation",
      "requirement": "Proper competition procedures",
      "status": "passed",
      "details": "All requirements met",
      "reference": "FAR Part 6"
    }
  ],
  "recommendations": ["Recommendation 1"]
}
```

### Proposals API

#### `GET /api/proposals`
List user's proposals.

**Headers:** `Authorization: Bearer TOKEN`

#### `POST /api/proposals`
Create new proposal.

**Headers:** `Authorization: Bearer TOKEN`

**Request:**
```json
{
  "title": "My Proposal",
  "opportunityId": "opp_uuid",
  "sections": [
    {
      "id": "executive_summary",
      "title": "Executive Summary",
      "required": true
    }
  ]
}
```

#### `PATCH /api/proposals/[id]`
Update proposal.

**Headers:** `Authorization: Bearer TOKEN`

#### `DELETE /api/proposals/[id]`
Delete proposal.

**Headers:** `Authorization: Bearer TOKEN`

### Documents API

#### `POST /api/documents/upload`
Upload document for parsing.

**Headers:** `Authorization: Bearer TOKEN`

**Content-Type:** `multipart/form-data`

**Response:**
```json
{
  "id": "doc_uuid",
  "name": "document.pdf",
  "s3_url": "https://...",
  "status": "processing"
}
```

---

## 🔧 Utility Functions

### Supabase Client (`lib/supabase.ts`)

```typescript
import { supabase, supabaseAdmin } from '@/lib/supabase';

// Client-side (RLS enforced)
const { data } = await supabase.from('proposals').select('*');

// Server-side (bypass RLS)
const { data } = await supabaseAdmin.from('grants').select('*');
```

### Auth Middleware (`lib/authMiddleware.ts`)

```typescript
import { requireAuth } from '@/lib/authMiddleware';

export default async function handler(req, res) {
  const authedReq = await requireAuth(req, res);
  if (!authedReq) return; // Already sent 401

  // Use authedReq.user
  console.log(authedReq.user.id);
}
```

### Document Parser (`lib/documentParser.ts`)

```typescript
import { parseDocument } from '@/lib/documentParser';

const parsed = await parseDocument('/path/to/file.pdf', 'pdf');
console.log(parsed.text);
console.log(parsed.metadata.wordCount);
```

---

## 🧪 Testing

### Manual Testing

```bash
# Test grants search
curl -X POST http://localhost:3000/api/grants/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "technology"}'

# Test with auth (get token from Supabase)
TOKEN="your_supabase_auth_token"
curl -X POST http://localhost:3000/api/proposals \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Test Proposal"}'
```

### Unit Tests (TODO)

```typescript
// tests/api/grants.test.ts
import { createMocks } from 'node-mocks-http';
import handler from '@/pages/api/grants/search';

test('searches grants successfully', async () => {
  const { req, res } = createMocks({
    method: 'POST',
    body: { keyword: 'research' }
  });

  await handler(req, res);
  expect(res._getStatusCode()).toBe(200);
});
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Unauthorized" errors**
- Check `Authorization: Bearer TOKEN` header
- Verify token is valid (not expired)
- Ensure RLS policies are correct

**2. "Failed to fetch" from external APIs**
- Verify API keys in `.env.local`
- Check API rate limits
- Review API endpoint URLs

**3. Document upload fails**
- Check Supabase Storage bucket exists (`documents`)
- Verify storage policies allow uploads
- Check file size limits

**4. Database errors**
- Ensure schema migration ran successfully
- Check table names and column names match
- Verify RLS policies don't block operations

---

## 📈 Next Steps

### Immediate (Week 1)
1. ✅ Run database migration
2. ✅ Configure environment variables
3. ✅ Test API endpoints
4. 🔲 Implement document parsing worker
5. 🔲 Set up Supabase Storage bucket

### Short-term (Week 2-3)
1. Integrate Grants.gov API (get API key)
2. Implement USASpending.gov sync
3. Add background job queue for document parsing
4. Set up monitoring and error tracking
5. Add API rate limiting

### Medium-term (Month 1-2)
1. Implement real-time collaboration (Supabase Realtime)
2. Add advanced analytics queries
3. Implement team permissions logic
4. Add webhook endpoints for external integrations
5. Build admin dashboard

---

## 📦 Dependencies

### Core
- `@supabase/supabase-js` - Database & auth
- `openai` - AI features
- `axios` - HTTP client

### Document Processing
- `pdf-parse` - PDF parsing
- `mammoth` - DOCX parsing
- `formidable` - File upload handling

### Utilities
- `uuid` - ID generation

---

## 🔒 Security Best Practices

1. **Never expose service role key** on client-side
2. **Always use RLS** for user-specific data
3. **Validate all inputs** in API routes
4. **Rate limit** external API calls
5. **Sanitize uploaded files** before processing
6. **Use prepared statements** for SQL queries
7. **Implement CORS** properly

---

## 📧 Support

Questions? Check:
- Supabase docs: https://supabase.com/docs
- OpenAI API docs: https://platform.openai.com/docs
- Next.js API routes: https://nextjs.org/docs/api-routes/introduction

---

**Backend implementation complete! Ready for frontend integration.** 🚀
