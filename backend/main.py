from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime

app = FastAPI(
    title="Sturgeon AI API",
    description="Government Contracting & Grant Management Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class OpportunitySearch(BaseModel):
    keywords: Optional[str] = "AI"
    limit: Optional[int] = 10
    agency: Optional[str] = None

class ContractAnalysis(BaseModel):
    contract_id: str
    contract_text: str

class ProposalGeneration(BaseModel):
    contract_id: str
    requirements: str
    company_info: Optional[str] = None

class OpportunityMatch(BaseModel):
    company_profile: str
    keywords: List[str]

# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# ==================== SAM.GOV INTEGRATION ====================

@app.get("/api/opportunities/search")
async def search_opportunities(keywords: str = "AI", limit: int = 10, agency: str = None):
    # Mock data for demo - replace with actual SAM.gov API call
    opportunities = [
        {
            "id": "SAM-2024-001",
            "title": f"Advanced {keywords} Solutions for Federal Agencies",
            "agency": agency or "Department of Defense",
            "type": "Contract",
            "value": "$2.5M - $5M",
            "deadline": "2025-12-15",
            "description": f"Development and deployment of {keywords}-powered systems",
            "naics_code": "541512",
            "set_aside": "8(a)",
            "posted_date": "2024-10-15"
        },
        {
            "id": "SAM-2024-002",
            "title": f"Cloud-Based {keywords} Platform",
            "agency": "General Services Administration",
            "type": "Contract",
            "value": "$1M - $3M",
            "deadline": "2025-11-30",
            "description": f"Scalable cloud infrastructure with {keywords} capabilities",
            "naics_code": "541519",
            "set_aside": "Small Business",
            "posted_date": "2024-10-20"
        }
    ]

    return {
        "success": True,
        "count": len(opportunities),
        "opportunities": opportunities[:limit]
    }

# ==================== GRANTS.GOV INTEGRATION ====================

@app.get("/api/grants/search")
async def search_grants(keywords: str = "technology", limit: int = 10):
    grants = [
        {
            "id": "GRANT-2024-001",
            "title": f"{keywords.title()} Innovation Grant",
            "agency": "National Science Foundation",
            "amount": "$500,000",
            "deadline": "2025-12-31",
            "description": f"Support for innovative {keywords} research and development",
            "eligibility": "Small businesses, universities, nonprofits"
        },
        {
            "id": "GRANT-2024-002",
            "title": f"Advanced {keywords.title()} Research",
            "agency": "Department of Energy",
            "amount": "$750,000",
            "deadline": "2025-11-15",
            "description": f"Cutting-edge {keywords} research initiatives",
            "eligibility": "Research institutions, small businesses"
        }
    ]

    return {
        "success": True,
        "count": len(grants),
        "grants": grants[:limit]
    }

# ==================== AI CONTRACT ANALYSIS ====================

@app.post("/api/ai/analyze-contract")
async def analyze_contract(data: ContractAnalysis):
    # Mock analysis - replace with OpenAI API call
    analysis = {
        "contract_id": data.contract_id,
        "summary": "This contract requires cloud infrastructure services with AI capabilities.",
        "key_requirements": [
            "FedRAMP authorization required",
            "24/7 support mandatory",
            "99.9% uptime SLA",
            "FISMA compliance",
            "Agile development methodology"
        ],
        "compliance_score": 85,
        "risk_factors": [
            "Tight delivery timeline",
            "Complex security requirements"
        ],
        "recommendations": [
            "Highlight existing FedRAMP authorization",
            "Emphasize proven government experience",
            "Include detailed security plan"
        ]
    }

    return {
        "success": True,
        "analysis": analysis
    }

# ==================== AI PROPOSAL GENERATION ====================

@app.post("/api/ai/generate-proposal")
async def generate_proposal(data: ProposalGeneration):
    # Mock generation - replace with OpenAI API call
    proposal = f'''# Technical Proposal for Contract {data.contract_id}

## Executive Summary
Our organization is uniquely qualified to deliver exceptional results for this critical project. 
With over 15 years of government contracting experience and deep expertise in the required 
technologies, we are the ideal partner.

## Technical Approach

### Solution Architecture
We propose a cloud-native, microservices-based architecture that ensures:
- Scalability to handle varying workloads
- High availability with 99.99% uptime
- Security by design with zero-trust principles
- Cost optimization through intelligent resource management

### Implementation Plan
Phase 1 (Months 1-3): Requirements analysis and design
Phase 2 (Months 4-6): Core development and testing
Phase 3 (Months 7-9): Deployment and optimization
Phase 4 (Ongoing): Support and enhancement

## Compliance & Security
- FedRAMP High authorized infrastructure
- FISMA compliant operations
- NIST 800-53 controls implementation
- Continuous monitoring and vulnerability management

## Team Qualifications
Our team brings exceptional credentials:
- 15+ years government contracting experience
- CMMI Level 3 certified organization
- ISO 27001 information security certified
- Security clearances: Top Secret/SCI available

## Past Performance
Successfully delivered 25+ government contracts totaling $50M+ in value with:
- 100% on-time delivery rate
- 98% customer satisfaction score
- Zero security incidents

## Pricing
We offer competitive pricing with flexible payment terms aligned with government fiscal 
year requirements. Detailed pricing breakdown available upon request.

## Requirements Compliance

{data.requirements}

We meet all stated requirements and exceed expectations in the following areas:
1. Advanced technical capabilities beyond baseline requirements
2. Experienced team with relevant clearances
3. Proven track record with similar projects
4. Innovative approach to problem-solving

## Conclusion
We are committed to delivering excellence and look forward to partnering on this 
critical initiative. Our combination of technical expertise, government experience, 
and commitment to quality makes us the ideal choice.
'''

    return {
        "success": True,
        "contract_id": data.contract_id,
        "proposal": proposal,
        "metadata": {
            "word_count": len(proposal.split()),
            "sections": 8,
            "generated_at": datetime.utcnow().isoformat()
        }
    }

# ==================== OPPORTUNITY MATCHING ====================

@app.post("/api/ai/match-opportunities")
async def match_opportunities(data: OpportunityMatch):
    # Mock matching algorithm
    matches = [
        {
            "opportunity_id": "SAM-2024-003",
            "title": "AI-Powered Analytics Platform",
            "match_score": 95,
            "reasons": [
                "Perfect alignment with company capabilities",
                "Matches NAICS codes",
                "Within typical contract size range"
            ]
        },
        {
            "opportunity_id": "SAM-2024-004",
            "title": "Cloud Infrastructure Services",
            "match_score": 88,
            "reasons": [
                "Strong technical fit",
                "Relevant past performance",
                "Appropriate set-aside category"
            ]
        }
    ]

    return {
        "success": True,
        "matches": matches
    }

# ==================== DOCUMENT UPLOAD ====================

@app.post("/api/documents/upload")
async def upload_document():
    return {
        "success": True,
        "file_id": "DOC-2024-001",
        "message": "Document uploaded successfully"
    }

# ==================== ANALYTICS DASHBOARD ====================

@app.get("/api/analytics/dashboard")
async def get_dashboard():
    return {
        "success": True,
        "metrics": {
            "total_proposals": 45,
            "active_opportunities": 23,
            "win_rate": 34.5,
            "total_value": 12500000,
            "monthly_stats": [
                {"month": "Jan", "proposals": 12, "wins": 4},
                {"month": "Feb", "proposals": 15, "wins": 5},
                {"month": "Mar", "proposals": 18, "wins": 7}
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
