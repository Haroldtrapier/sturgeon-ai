# 🐟 Sturgeon AI - Government Contracting & Grants Intelligence Platform

![Sturgeon AI](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)
![React](https://img.shields.io/badge/React-18-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Sturgeon AI** is a comprehensive AI-powered platform designed to help businesses navigate federal contracting and grants opportunities. Built specifically for Service-Disabled Veteran-Owned Small Businesses (SDVOSBs), small businesses, and grant seekers.

## ✨ Features

### Core Capabilities
- 🔍 **Smart Opportunity Search**: Search SAM.gov and Grants.gov with advanced filters (NAICS, set-asides, agencies)
- 🤖 **AI Contract Analysis**: Automatically analyze solicitations for requirements, risks, and win factors
- 📝 **Proposal Generation**: Generate compliant, persuasive proposals with AI assistance
- 🎯 **Intelligent Matching**: AI-powered opportunity matching based on your history and capabilities
- 📊 **Analytics Dashboard**: Track performance metrics, win rates, and agency-specific insights
- 💼 **Company Profile Management**: Store certifications, NAICS codes, past performance

### AI-Powered Features
- Contract requirement extraction and analysis
- Risk assessment and mitigation strategies
- NAICS code recommendations
- Win theme identification
- Proposal writing assistance
- Opportunity scoring and ranking

## 🏗️ Architecture

```
sturgeon-ai/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── models.py        # Database models
│   ├── database.py      # Database configuration
│   ├── auth.py          # Authentication utilities
│   ├── config.py        # Application settings
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend container
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/      # Page components
│   │   ├── components/ # Reusable components
│   │   └── App.tsx     # Main app component
│   ├── package.json
│   └── Dockerfile       # Frontend container
├── docker-compose.yml   # Full stack orchestration
├── .env.example         # Environment template
└── README.md           # This file
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: ORM for database operations
- **OpenAI GPT**: AI-powered analysis and generation
- **SAM.gov API**: Federal contracting opportunities
- **Grants.gov API**: Federal grant opportunities

### Frontend
- **React 18**: Modern UI library
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **TanStack Query**: Data fetching and caching
- **Tailwind CSS**: Utility-first styling
- **Zustand**: State management

### Infrastructure
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **PostgreSQL**: Production database

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- SAM.gov API key ([Get it here](https://open.gsa.gov/api/sam-gov-entity-api/))
- OpenAI API key ([Get it here](https://platform.openai.com/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Haroldtrapier/sturgeon-ai.git
cd sturgeon-ai
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys:
# - SAM_API_KEY
# - OPENAI_API_KEY
# - SECRET_KEY (change to a secure random string)
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the application**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs
- 🗄️ Database: localhost:5432

### Local Development (Without Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔑 API Keys Setup

### SAM.gov API Key
1. Register at https://sam.gov/
2. Request API access at https://open.gsa.gov/api/sam-gov-entity-api/
3. Add to `.env`: `SAM_API_KEY=your_key_here`

### OpenAI API Key
1. Sign up at https://platform.openai.com/
2. Create an API key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`

## 📖 API Documentation

### Search Opportunities
```bash
POST /api/opportunities/search
{
  "keywords": "cybersecurity",
  "naics_codes": ["541512"],
  "set_asides": ["SDVOSB"],
  "limit": 25
}
```

### AI Contract Analysis
```bash
POST /api/ai/analyze-contract
{
  "title": "IT Services Contract",
  "agency": "Department of Defense",
  "body": "Full solicitation text..."
}
```

### Generate Proposal
```bash
`POST /api/ai/generate-proposal
{
  "opportunity": {...},
  "company_profile": {
    "name": "ABC Corp",
    "certifications": ["SDVOSB"],
    "capabilities": "..."
  }
}
```

### View Full API Documentation
Visit http://localhost:8000/docs for interactive API documentation.

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Run all tests
docker-compose run backend pytest
docker-compose run frontend npm test
```

## 🚀 Deployment

### Docker Production Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment Options
- **AWS**: ECS, RDS, CloudFront
- **Google Cloud**: Cloud Run, Cloud SQL, Cloud CDN
- **Azure**: App Service, Azure Database, Azure CDN
- **Heroku**: Easy deployment with PostgreSQL add-on

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- SAM.gov for federal contracting data
- Grants.gov for federal grant information
- OpenAI for AI capabilities
- The open-source community

## 📧 Contact

Harold - [@Haroldtrapier](https://github.com/Haroldtrapier)

Project Link: [https://github.com/Haroldtrapier/sturgeon-ai](https://github.com/Haroldtrapier/sturgeon-ai)

## 🗺️ Roadmap

- [ ] Advanced proposal templates library
- [ ] Email notifications for matching opportunities
- [ ] Integration with proposal management tools
- [ ] Mobile application (iOS & Android)
- [ ] Advanced analytics and reporting
- [ ] Team collaboration features
- [ ] Document generation (Word, PDF exports)
- [ ] Compliance checking automation
- [ ] Integration with accounting systems
- [ ] Calendar synchronization for deadlines

## 💡 Use Cases

### For Small Businesses
- Find relevant contracting opportunities
- Understand complex solicitations
- Generate competitive proposals quickly
- Track win rates and improve strategies

### For SDVOSBs
- Target set-aside opportunities
- Leverage veteran status effectively
- Build competitive proposals highlighting veteran ownership
- Track performance with veteran-focused agencies

### For Grant Seekers
- Discover federal grant opportunities
- Analyze grant requirements
- Generate compelling grant proposals
- Monitor grant deadlines

## 💒 Security

- Environment variables for sensitive data
- JWT-based authentication
- PostgreSQL with secure connections
- HTTPS in production (recommended)
- Regular security audits

## 📊 Performance

- FastAPI async endpoints for high concurrency
- Database connection pooling
- React query caching
- Optimized Docker images
- CDN-ready static assets

---

**Built with ❤️ for the federal contracting community**

*Empowering small businesses to win government contracts*