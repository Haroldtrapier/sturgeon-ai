# Sturgeon AI Backend API

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
OPENAI_API_KEY=your_key
SAM_GOV_API_KEY=your_key
GRANTS_GOV_API_KEY=your_key
```

3. Run the server:
```bash
uvicorn main:app --reload
```

## API Endpoints

- GET `/health` - Health check
- GET `/api/opportunities/search` - Search SAM.gov contracts
- GET `/api/grants/search` - Search Grants.gov grants
- POST `/api/ai/analyze-contract` - Analyze contract requirements
- POST `/api/ai/generate-proposal` - Generate AI proposal
- POST `/api/ai/match-opportunities` - Match opportunities to profile
- POST `/api/documents/upload` - Upload documents
- GET `/api/analytics/dashboard` - Get analytics data

## Deployment

Deploy to Vercel with:
```bash
vercel --prod
```
