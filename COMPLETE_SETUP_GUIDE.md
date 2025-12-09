# 🚀 Sturgeon AI - Complete Setup & Deployment Guide

## 📋 Table of Contents

1. [Quick Start (15 minutes)](#quick-start)
2. [Detailed Setup](#detailed-setup)
3. [Testing](#testing)
4. [Deployment](#deployment)
5. [Troubleshooting](#troubleshooting)
6. [Production Checklist](#production-checklist)

---

## 🎯 Quick Start

Get Sturgeon AI running locally in 15 minutes:

### Step 1: Run Setup Script (5 min)

```bash
# Clone and enter directory
cd sturgeon-ai

# Run automated setup
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This installs dependencies and creates `.env.local` template.

### Step 2: Configure Environment (3 min)

Edit `.env.local`:

```bash
# REQUIRED - Get from Supabase Dashboard
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_KEY=eyJhbG...

# REQUIRED - Get from OpenAI Platform
OPENAI_API_KEY=sk-...

# OPTIONAL - Can add later
GRANTS_GOV_API_KEY=...
```

### Step 3: Setup Database (5 min)

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project → SQL Editor
3. Copy contents of `database/schema.sql`
4. Paste and click "Run"
5. Should see: "Success. No rows returned"

### Step 4: Create Storage Bucket (2 min)

1. Supabase Dashboard → Storage
2. Click "Create Bucket"
3. Name: `documents`
4. Public: Toggle ON (or configure RLS later)
5. Click "Create Bucket"

### Step 5: Start Development Server

```bash
npm run dev
```

Visit: http://localhost:3000

**✅ You're done! Start testing features.**

---

## 🔧 Detailed Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- Supabase account
- OpenAI API key

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/HaroldtrapieR/sturgeon-ai.git
cd sturgeon-ai
```

#### 2. Install Dependencies

```bash
# Core dependencies
npm install

# Additional packages (if not already in package.json)
npm install @supabase/supabase-js openai axios
npm install formidable pdf-parse mammoth uuid
npm install -D @types/formidable @types/uuid

# Testing (optional)
npm install -D jest ts-jest @types/jest node-mocks-http
```

#### 3. Environment Configuration

**Copy template:**
```bash
cp .env.example .env.local
```

**Fill in values:**

| Variable | Where to Get It | Required |
|----------|-----------------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase Dashboard → Settings → API | ✅ Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase Dashboard → Settings → API | ✅ Yes |
| `SUPABASE_SERVICE_KEY` | Supabase Dashboard → Settings → API → service_role | ✅ Yes |
| `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) | ✅ Yes |
| `GRANTS_GOV_API_KEY` | [Grants.gov](https://www.grants.gov/web/grants/support/web-services.html) | ⚪ Optional |

#### 4. Database Setup

**Option A: Supabase Dashboard (Recommended)**
1. Go to your Supabase project
2. SQL Editor → New Query
3. Copy-paste `database/schema.sql`
4. Click RUN

**Option B: psql Command Line**
```bash
psql $DATABASE_URL -f database/schema.sql
```

**Verify:**
```sql
-- Run in SQL Editor
SELECT COUNT(*) FROM information_schema.tables 
WHERE table_schema = 'public';
-- Should return 12 (or more)
```

#### 5. Supabase Storage Setup

**Create documents bucket:**

1. Dashboard → Storage → New Bucket
2. Name: `documents`
3. Public: ON (for easy testing)
4. Click Create

**Configure RLS (Production):**
```sql
-- Allow authenticated users to upload
CREATE POLICY "Users can upload documents"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'documents' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Allow users to read their own documents
CREATE POLICY "Users can read own documents"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'documents' AND auth.uid()::text = (storage.foldername(name))[1]);
```

---

## 🧪 Testing

### Manual API Testing

```bash
# Test grants search (no auth required)
curl -X POST http://localhost:3000/api/grants/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "research"}'

# Expected: {"grants": [...]}
```

**With Authentication:**

1. Get auth token:
   - Supabase Dashboard → Authentication → Users
   - Click on user → Copy Access Token

2. Test protected endpoint:
```bash
TOKEN="your_access_token_here"

curl -X POST http://localhost:3000/api/proposals \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Proposal"}'
```

### Automated Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode (for development)
npm run test:watch
```

### Component Testing (Frontend)

```bash
# Install testing library
npm install -D @testing-library/react @testing-library/jest-dom

# Run component tests
npm test components/
```

---

## 🚀 Deployment

### Deploy to Vercel (Recommended)

**Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

**Step 2: Login**
```bash
vercel login
```

**Step 3: Deploy**
```bash
# First deployment
vercel

# Production deployment
vercel --prod
```

**Step 4: Add Environment Variables**

In Vercel Dashboard:
1. Project → Settings → Environment Variables
2. Add all variables from `.env.local`
3. Redeploy

**Automatic Deployments:**
- Push to `main` → Production
- Push to other branches → Preview

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

### Deploy with Docker

```bash
# Build image
docker build -t sturgeon-ai .

# Run container
docker run -p 3000:3000 --env-file .env.local sturgeon-ai

# Or use docker-compose
docker-compose up
```

### Background Worker Deployment

**Vercel (Serverless Cron):**
Create `vercel.json`:
```json
{
  "crons": [{
    "path": "/api/cron/process-documents",
    "schedule": "*/5 * * * *"
  }]
}
```

**Separate Service (Recommended for high volume):**
```bash
# Deploy worker separately
docker build -f Dockerfile.worker -t sturgeon-worker .
docker run sturgeon-worker
```

---

## 🐛 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

#### Database connection fails
- Check Supabase project is not paused
- Verify URL and keys are correct
- Test connection in SQL Editor

#### 401 Unauthorized on API calls
- Get fresh auth token from Supabase
- Check token is in `Authorization: Bearer TOKEN` format
- Verify RLS policies are correct

#### Document upload fails
- Ensure `documents` bucket exists
- Check storage policies
- Verify file size limits (default 50MB)

#### OpenAI API errors
- Check API key is valid
- Verify you have credits
- Check rate limits

### Debug Mode

Enable verbose logging:

```bash
# .env.local
DEBUG=true
LOG_LEVEL=debug
```

### Health Check Endpoint

Create `pages/api/health.ts`:
```typescript
export default function handler(req, res) {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    database: 'connected', // Add actual check
    storage: 'connected'   // Add actual check
  });
}
```

---

## ✅ Production Checklist

### Security

- [ ] Environment variables are set in production
- [ ] Service role key is not exposed to client
- [ ] RLS policies are enabled on all user tables
- [ ] API rate limiting is configured
- [ ] CORS is properly configured
- [ ] File upload size limits are set
- [ ] Input validation on all API routes
- [ ] SQL injection prevention (use parameterized queries)

### Performance

- [ ] Database indexes are created
- [ ] API routes have caching where appropriate
- [ ] Images are optimized
- [ ] Code splitting is enabled
- [ ] Bundle size is optimized

### Monitoring

- [ ] Error tracking (Sentry, LogRocket)
- [ ] Analytics (Mixpanel, PostHog)
- [ ] Uptime monitoring (Better Uptime)
- [ ] Performance monitoring (Vercel Analytics)
- [ ] Database monitoring (Supabase Dashboard)

### Backups

- [ ] Database backups are enabled (Supabase automatic)
- [ ] Storage backups are configured
- [ ] Environment variables are documented

### Documentation

- [ ] API documentation is up to date
- [ ] Component documentation exists
- [ ] Deployment process is documented
- [ ] Environment variables are documented

---

## 📚 Additional Resources

### Documentation
- [Supabase Docs](https://supabase.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)

### Support
- GitHub Issues: [Report bugs](https://github.com/HaroldtrapieR/sturgeon-ai/issues)
- Discussions: [Ask questions](https://github.com/HaroldtrapieR/sturgeon-ai/discussions)

---

## 🎉 You're Ready!

Your Sturgeon AI platform is now:
- ✅ Fully set up locally
- ✅ Ready for testing
- ✅ Prepared for deployment
- ✅ Production-ready

**Next steps:**
1. Test all features thoroughly
2. Get Grants.gov API key
3. Deploy to production
4. Monitor and iterate

**Need help?** Check the troubleshooting section or open an issue!
