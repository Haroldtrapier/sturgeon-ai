# Sturgeon AI - Government Contracting Platform

## 🚀 Fully Functional AI-Powered Platform

Complete government contracting platform with authentication, dashboard, and 5 specialized AI agents.

## ✨ Features

### 🔐 Authentication System
- Email/Password signup & login
- Supabase backend
- Auto-confirmed emails (no verification needed)
- Protected routes

### 📊 Dashboard
- User profile management
- Stats & metrics display
- Contracts table
- Opportunities cards
- Search functionality
- Settings page
- Responsive sidebar navigation

### 🤖 AI Chat with 5 Specialized Agents

1. **General Assistant** 🤖
   - General government contracting help
   - Strategy and advice

2. **Contract Analyzer** 📊
   - Analyzes RFPs and contracts
   - Identifies requirements
   - Provides compliance insights

3. **Proposal Writer** ✍️
   - Helps write winning proposals
   - Creates win themes
   - Generates compliance matrices

4. **Compliance Checker** ✅
   - Checks FAR/DFARS compliance
   - Identifies risks
   - Provides corrective actions

5. **Opportunity Finder** 🎯
   - Finds relevant SAM.gov opportunities
   - Matches company capabilities
   - Deadline tracking

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Authentication**: Supabase Auth
- **Database**: PostgreSQL (Supabase)
- **AI**: OpenAI GPT-4
- **Styling**: Tailwind CSS
- **Deployment**: Vercel

## 📦 Setup Instructions

### 1. Clone & Install

\`\`\`bash
git clone https://github.com/Haroldtrapier/sturgeon-ai.git
cd sturgeon-ai
npm install
\`\`\`

### 2. Environment Variables

Create `.env.local`:

\`\`\`env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# OpenAI
OPENAI_API_KEY=your_openai_api_key
\`\`\`

### 3. Supabase Setup

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Copy your project URL and keys
4. Database is auto-configured (auth.users table)

### 4. OpenAI Setup

1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an API key
3. Add to environment variables

### 5. Deploy to Vercel

\`\`\`bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add environment variables in Vercel dashboard
# Settings → Environment Variables
\`\`\`

## 🧪 Testing

1. **Signup**: Visit `/signup` and create an account
2. **Login**: Visit `/login` with your credentials
3. **Dashboard**: View stats, contracts, opportunities
4. **AI Chat**: Click "🤖 AI Chat" in sidebar
5. **Select Agent**: Choose from 5 specialized agents
6. **Start Chatting**: Ask questions, get AI responses

## 📱 Pages

- `/` - Home (redirects to dashboard if logged in)
- `/signup` - Create account
- `/login` - Sign in
- `/dashboard` - Main dashboard
- `/ai-chat` - AI agents interface
- `/forgot-password` - Password reset (placeholder)

## 🔧 API Endpoints

- `POST /api/auth/register` - User signup
- `POST /api/auth/login` - User login
- `POST /api/ai/chat` - AI chat with agents

## 🎯 AI Agent Prompts

Each agent has specialized system prompts:
- **Contract Analyzer**: Expert RFP/contract analysis
- **Proposal Writer**: Compelling proposal creation
- **Compliance Checker**: FAR/DFARS compliance verification
- **Opportunity Finder**: SAM.gov opportunity discovery
- **General**: Overall government contracting assistance

## 🚀 What's Working

✅ User authentication (signup/login)
✅ Protected dashboard
✅ Full-featured UI with stats & tables
✅ 5 AI agents with specialized knowledge
✅ Real-time chat interface
✅ Conversation history display
✅ Responsive design
✅ Search functionality
✅ Settings management

## 📝 TODO / Future Enhancements

- [ ] Connect to real SAM.gov API
- [ ] Store conversation history in database
- [ ] Add file upload for document analysis
- [ ] Implement advanced analytics
- [ ] Add email notifications
- [ ] Multi-user workspace management
- [ ] Export proposals to PDF
- [ ] Integration with procurement systems

## 🆘 Troubleshooting

### AI Chat Not Working
- **Check OpenAI API Key**: Ensure `OPENAI_API_KEY` is set in Vercel env vars
- **Check Console**: Look for error messages in browser DevTools
- **API Limits**: Verify OpenAI API quota/billing

### Auth Not Working
- **Check Supabase Keys**: Verify all 3 Supabase env vars are set
- **Email Confirmation**: Already disabled (auto-confirmed)
- **Clear Cookies**: Try incognito/private browsing

### Dashboard Empty
- **Login First**: Must be authenticated to access
- **Hard Refresh**: Cmd+Shift+R to clear cache

## 📄 License

MIT

## 👨‍💻 Author

Built with ❤️ by Sturgeon AI Team

---

**Ready to revolutionize government contracting with AI!** 🚀
\`\`\`
