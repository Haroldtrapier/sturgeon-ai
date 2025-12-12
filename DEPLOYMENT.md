# Deployment Guide

## Quick Deploy to Vercel

### 1. Frontend Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
vercel --prod

# Set environment variables in Vercel dashboard:
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
```

### 2. Backend Deployment

```bash
cd backend

# Deploy backend
vercel --prod

# Set environment variables in Vercel dashboard:
OPENAI_API_KEY=your_key
SAM_GOV_API_KEY=your_key
GRANTS_GOV_API_KEY=your_key
DATABASE_URL=your_supabase_url
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
ADMIN_SECRET_KEY=your_admin_secret
ADMIN_BEARER_TOKEN=your_admin_bearer_token
```

### 3. Connect Frontend to Backend

Update `NEXT_PUBLIC_API_URL` in frontend Vercel settings to point to your backend URL.

## Database Setup (Supabase)

1. Create Supabase project
2. Copy connection URL
3. Add to backend environment variables
4. Tables are auto-created on first API call

## External APIs Setup

### SAM.gov API
1. Register at https://sam.gov/
2. Get API key from account settings
3. Add to backend `.env`

### Grants.gov (No key needed)
Uses public search endpoints

### OpenAI API
1. Get key from https://platform.openai.com/
2. Add to backend `.env`

## Monitoring

- Frontend: Vercel Analytics
- Backend: Vercel Logs
- Database: Supabase Dashboard

## Production Checklist

- [ ] Environment variables set
- [ ] Database configured
- [ ] API keys added
- [ ] CORS configured
- [ ] SSL certificates active
- [ ] Monitoring enabled
- [ ] Backup strategy in place
