# Sturgeon AI - Complete Production Setup

A production-ready full-stack application with Next.js frontend, FastAPI backend, Supabase database, and Stripe payments.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Supabase account
- Stripe account

### 1. Database Setup (5 minutes)

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project: `sturgeon-ai`
3. Navigate to SQL Editor
4. Run the contents of `database.sql`

### 2. Install Dependencies (5 minutes)

**Frontend:**
```bash
npm install
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Setup

**Backend (.env):**
- Copy `backend/.env` and update with your credentials
- Get Supabase URL from Project Settings → API
- Generate JWT secret: `openssl rand -hex 32`
- Add your Stripe keys from Stripe Dashboard

**Frontend (.env.local):**
- Copy `.env.local` and update
- Add your Stripe publishable key

### 4. Start the Application (2 minutes)

**Backend:**
```bash
cd backend
python main.py
```

**Frontend:**
```bash
npm run dev
```

### 5. Access the App

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📋 Next Steps

✅ Create your first user via /signup
✅ Test the login flow
✅ Try the payment checkout
✅ Customize the UI
✅ Add your business logic
✅ Deploy to production

## 🔗 Resources

- [Recipe on Rube](https://rube.app/recipes/024033c5-fc4e-48a0-a6e8-98b16dd6b8ca)
- [Supabase Docs](https://supabase.com/docs)
- [Stripe Docs](https://stripe.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)

## 🛠️ Tech Stack

- **Frontend:** Next.js 14, React 18, Tailwind CSS
- **Backend:** FastAPI, JWT Auth, Bcrypt
- **Database:** Supabase PostgreSQL
- **Payments:** Stripe Integration

## 📝 License

MIT
