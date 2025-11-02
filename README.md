# 🚀 Sturgeon AI - Government Contracting Platform v2.0

**Production-Ready** | **Secure Authentication** | **Stripe Payments** | **Enterprise Features**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security: A+](https://img.shields.io/badge/Security-A+-brightgreen.svg)](SECURITY.md)
[[Deploy: Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com)

---

## 🎉️ What's New in v2.0?

### ✅ **Real Authentication**
- JWT token-based auth
- Bcrypt password hashing
- Secure session management
- Protected API endpoints

### ✅ **Stripe Payment Integration**
- Subscription management
- Multiple pricing tiers
- Secure checkout flow
- Webhook support

### ✅ **Production Database**
- Supabase PostgreSQL
- Row Level Security
- Data persistence
- Backup & recovery

### ✅ **Security Hardening**
- Rate limiting
- CORS protection
- Input validation
- SQL injection prevention

---

## 🏗️ Architecture

```
┌────────────────┐      ┌─────────────────┐      ┌───────────────┐
│   Frontend      │
─────┴▚│   FastAPI        │────┴▚│   Supabase      │
│   Next.js 14   |      │   Backend        │      │   PostgreSQL    │
│   + Tailwind    │◀────┘│   + Auth         │      └────────────────┘│   + Stripe       │                         │
└────────────────┘ │   + Payments     |      └────────────────┘                   │
                      │                                            │
                      └───────────────────────────────────┘
                                  Secure TLS 1.3
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Supabase account
- Stripe account

### 1. Clone Repository
```bash
git clone https://github.com/Haroldtrapier/sturgeon-ai.git
cd sturgeon-ai
```

### 2. Setup Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn main:app --reload
```

### 3. Setup Frontend
```bash
npm install
cp .env.example .env.local
# Edit .env.local with your API URL
npm run dev
```

### 4. Open Browser
```
Frontend: http://localhost:3000
Backend: http://localhost:8000/docs
```

---

## 📖 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- **[SECURITY.md](SECURITY,�d)** - Security features & best practices
- **[API.md](API.md)** - API documentation

---

## 🔐 Security Features

| Feature | Status |
|---------|--------|
| JWT Authentication | ✅ |
| Password Hashing | ✅ Bcrypt |
| Rate Limiting | ✅ 10/min |
| CORS Protection | ✅ Whitelisted |
| SQL Injection | ✅ Protected |
| XSS Protection | ✅ React |
| CSRF Protection | ✅ JWT |
| Payment Security | ✅ Stripe PCI-DSS |

**Security Grade: A+** (Production Ready)

---

## 💳 Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $29/mo | 10 Proposals, Basic AI |
| **Pro** | $99/mo | Unlimited, Advanced AI |
| **Enterprise** | $299/mo | Custom Integration, SLA |

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Styling**: Tailwind CSS
- **Payments**: Stripe React
- **HTTP**: Axios
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI
- **Auth**: Python-Jose + Passlib
- **Database**: Supabase (PostgreSQL)
- **Payments**: Stripe Python
- _SPecurity**: SlowAPI (Rate Limiting)
- **Deployment**: Vercel

---

## 📊 API Endpoints

### Authentication
- POST /api/auth/register - Create account
- POST /api/auth/login - Login
- GET /api/auth/me - Get user info

### Payments
- POST /api/payments/create-payment-intent - One-time payment
- POST /api/payments/create-subscription - Start subscription
- GET /api/payments/subscription-status - Check status

### Protected Endpoints (Require Auth)
- GET /api/opportunities/search - Search contracts
- POST /api/ai/generate-proposal - AI proposal

[Full API Documentation →](API.md)

---

## 🧪 Testing

### Test Account
```
Email: test@example.com
Password: testpass123
```

### Stripe Test Card
```
Card: 4242 4242 4242 4242
Expiry: Any future date
CVC: Any 3 digits
```

---

## 📈 Roadmap

- [x] v1.0 - MVP (Demo)
- [x] v2.0 - Production (Auth + Payments)
- [ ] v2.1 - Email notifications
- [ ] v2.2 - Team collaboration
- [ ] v2.3 - Advanced analytics
- [ ] v3.0 - Mobile app

---

## 🤢 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

## 📞 Support

- **Email**: support@sturgeonai.com
- **Docs**: https://docs.sturgeonai.com
- **Issues**: https://github.com/Haroldtrapier/sturgeon-ai/issues

---

**Built with ❤️ by the Sturgeon AI Team**

[Website](https://sturgeonai.com) • [Twitter](https://twitter.com/sturgeonai) ~ [LinkedIn](https://linkedin.com/company/sturgeonai)
