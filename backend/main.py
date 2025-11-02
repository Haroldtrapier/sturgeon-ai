from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import stripe
from slowapi import Limiter
from slowapi.util import get_remote_address
from supabase import create_client, Client

load_dotenv()

# Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-prod")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPEE_PUBLISHABLE_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Sturgeon AI API v2.0",
    description="Production-ready with Auth & Payments",
    version="2.0.0"
)

app.state.limiter = limiter

# CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

# Security functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        if supabase:
            user = supabase.table("users").select("*").eq("email", email).execute()
            if user.data:
                return user.data[0]
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "features": {"auth": True, "payments": True, "database": supabase is not None}
    }

# Register
@app.post("/api/auth/register", response_model=Token)
@limiter.limit("5/minute")
async def register(user: UserCreate, request):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")
    
    existing = supabase.table("users").select("email").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email exists")
    
    hashed = get_password_hash(user.password)
    new_user = supabase.table("users").insert({
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hashed,
        "created_at": datetime.utcnow().isoformat()
    }).execute()
    
    token = create_access_token({"sub": user.email})
    user_data = new_user.data[0]
    user_data.pop("hashed_password", None)
    
    return {"access_token": token, "token_type": "bearer", "user": user_data}

# Login
@app.post("/api/auth/login", response_model=Token)
@limiter.limit("10/minute")
async def login(form: OAuth2PasswordRequestForm = Depends(), request=None):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")
    
    user = supabase.table("users").select("*").eq("email", form.username).execute()
    if not user.data or not verify_password(form.password, user.data[0]["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.data[0]["email"]})
    user_data = user.data[0]
    user_data.pop("hashed_password", None)
    
    return {"access_token": token, "token_type": "bearer", "user": user_data}

# Get current user
@app.get("/api/auth/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user

# Create payment
@app.post("/api/payments/create-payment-intent")
async def create_payment(data: dict, current_user: dict = Depends(get_current_user)):
    try:
        intent = stripe.PaymentIntent.create(
            amount=data.get("amount", 2900),
            currency="usd",
            metadata={"user_id": current_user.get("id")}
        )
        return {"client_secret": intent.client_secret, "publishable_key": STRIPE_PUBLISHABLE_KEY}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Create subscription
@app.post("/api/payments/create-subscription")
async def create_subscription(data: dict, current_user: dict = Depends(get_current_user)):
    try:
        customer = stripe.Customer.create(
            email=current_user.get("email"),
            payment_method=data["payment_method_id"],
            invoice_settings={"default_payment_method": data["payment_method_id"]}
        )
        
        sub = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": data["price_id"]}],
            expand=["latest_invoice.payment_intent"]
        )
        
        if supabase:
            supabase.table("subscriptions").insert({
                "user_id": current_user.get("id"),
                "stripe_subscription_id": sub.id,
                "stripe_customer_id": customer.id,
                "status": sub.status,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
        
        return {"subscription_id": sub.id, "status": sub.status}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get subscription status
@app.get("/api/payments/subscription-status")
async def subscription_status(current_user: dict = Depends(get_current_user)):
    if not supabase:
        return {"has_subscription": False}
    
    sub = supabase.table("subscriptions").select("*").eq("user_id", current_user.get("id")).execute()
    return {"has_subscription": bool(sub.data), "subscription": sub.data[0] if sub.data else None}

# Protected: Search opportunities
@app.get("/api/opportunities/search")
async def search_opportunities(keywords: str = "AI", limit: int = 10, current_user: dict = Depends(get_current_user)):
    opportunities = [
        {
            "id": "SAM-2024-001",
            "title": f"Advanced {keywords} Solutions",
            "agency": "DOD",
            "value": "$2.5M - $5M",
            "deadline": "2025-12-15"
        }
    ]
    return {"success": True, "opportunities": opportunities[:limit]}

# Protected: Generate proposal
@app.post("/api/ai/generate-proposal")
async def generate_proposal(data: dict, current_user: dict = Depends(get_current_user)):
    proposal = f"# Proposal for {data.get('contract_id')}\n\n## Requirements\n{data.get('requirements')}"
    return {"success": True, "proposal": proposal}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
