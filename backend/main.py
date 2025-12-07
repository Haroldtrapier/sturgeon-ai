from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from typing import Optional
import stripe

# Import marketing agent
from marketing_agent import marketing_director

# Initialize FastAPI
app = FastAPI(title="Sturgeon AI API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey123")
ALGORITHM = "HS256"
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Helper functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/")
async def root():
    return {"message": "Sturgeon AI API", "status": "online"}

@app.post("/auth/register", response_model=Token)
async def register(user: UserCreate):
    # In production, save to Supabase database
    hashed = hash_password(user.password)
    access_token = create_access_token({"sub": "user_id", "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
async def login(user: UserLogin):
    # In production, verify against database
    access_token = create_access_token({"sub": "user_id", "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def get_user_profile(current_user = Depends(get_current_user)):
    return current_user

@app.post("/payments/create-checkout")
async def create_checkout_session(current_user = Depends(get_current_user)):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Sturgeon AI Pro'},
                    'unit_amount': 2900,
                    'recurring': {'interval': 'month'},
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{os.getenv('FRONTEND_URL')}/success",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Marketing Agent Endpoints (Internal Use Only - Trapier Management LLC)
@app.get("/marketing/agent/info")
async def get_marketing_agent_info(current_user = Depends(get_current_user)):
    """Get Marketing Director Agent system information"""
    return {
        "agent": "Marketing Director for Sturgeon AI",
        "organization": "Trapier Management LLC",
        "purpose": "Internal marketing strategy and campaign execution",
        "capabilities": [
            "Campaign Strategy Development",
            "Content Creation",
            "Lead Generation",
            "Analytics & Optimization",
            "Competitive Intelligence",
            "Sales Enablement"
        ],
        "available_campaigns": marketing_director.get_all_campaigns(),
        "available_personas": marketing_director.get_all_personas(),
        "available_channels": marketing_director.get_all_channels()
    }

@app.get("/marketing/campaigns")
async def get_all_campaigns(current_user = Depends(get_current_user)):
    """Get all available marketing campaign templates"""
    return {
        "campaigns": marketing_director.campaign_templates,
        "total_count": len(marketing_director.campaign_templates)
    }

@app.get("/marketing/campaigns/{campaign_type}")
async def get_campaign_template(campaign_type: str, current_user = Depends(get_current_user)):
    """Get a specific campaign template"""
    template = marketing_director.get_campaign_template(campaign_type)
    if not template:
        raise HTTPException(status_code=404, detail=f"Campaign type '{campaign_type}' not found")
    return template

@app.get("/marketing/personas")
async def get_all_personas(current_user = Depends(get_current_user)):
    """Get all target audience personas"""
    return {
        "personas": marketing_director.personas,
        "total_count": len(marketing_director.personas)
    }

@app.get("/marketing/personas/{persona_type}")
async def get_persona(persona_type: str, current_user = Depends(get_current_user)):
    """Get a specific target audience persona"""
    persona = marketing_director.get_persona(persona_type)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona type '{persona_type}' not found")
    return persona

@app.get("/marketing/channels")
async def get_all_channels(current_user = Depends(get_current_user)):
    """Get all channel strategies"""
    return {
        "channels": marketing_director.channel_strategies,
        "total_count": len(marketing_director.channel_strategies)
    }

@app.get("/marketing/channels/{channel}")
async def get_channel_strategy(channel: str, current_user = Depends(get_current_user)):
    """Get a specific channel strategy"""
    strategy = marketing_director.get_channel_strategy(channel)
    if not strategy:
        raise HTTPException(status_code=404, detail=f"Channel '{channel}' not found")
    return strategy

@app.get("/marketing/metrics")
async def get_all_metrics(current_user = Depends(get_current_user)):
    """Get all marketing metrics and targets"""
    return marketing_director.get_metrics()

@app.get("/marketing/metrics/{category}")
async def get_metrics_by_category(category: str, current_user = Depends(get_current_user)):
    """Get metrics for a specific category (acquisition, engagement, revenue)"""
    metrics = marketing_director.get_metrics(category)
    if not metrics:
        raise HTTPException(status_code=404, detail=f"Metric category '{category}' not found")
    return metrics

@app.post("/marketing/campaign-brief")
async def generate_campaign_brief(
    campaign_type: str,
    persona_type: str,
    current_user = Depends(get_current_user)
):
    """
    Generate a complete campaign brief combining template, persona, and channel strategy
    
    Example: POST /marketing/campaign-brief?campaign_type=linkedin_outreach&persona_type=bd_director
    """
    try:
        brief = marketing_director.generate_campaign_brief(campaign_type, persona_type)
        return brief
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/marketing/system-prompt")
async def get_system_prompt(current_user = Depends(get_current_user)):
    """Get the complete Marketing Director Agent system prompt"""
    return {
        "system_prompt": marketing_director.system_prompt,
        "note": "Internal use only - Trapier Management LLC"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
