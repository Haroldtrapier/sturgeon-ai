from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from typing import Optional
import stripe
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

# Initialize Sentry (optional - only if SENTRY_DSN is set)
if sentry_dsn := os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            StarletteIntegration(transaction_style="url"),
            FastApiIntegration(transaction_style="url"),
        ],
        traces_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "production"),
    )

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])

# Initialize FastAPI
app = FastAPI(title="Sturgeon AI API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - LOCKED DOWN FOR PRODUCTION
# Only allow requests from your production domains
ALLOWED_ORIGINS = [
    "https://sturgeon-ai-prod.vercel.app",
    "https://sturgeon-ai.vercel.app",
    # Add your custom domain when you set it up:
    # "https://sturgeonai.com",
    # "https://www.sturgeonai.com",
]

# Allow localhost in development only
if os.getenv("ENVIRONMENT") == "development":
    ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Explicit methods instead of "*"
    allow_headers=["Content-Type", "Authorization"],  # Explicit headers instead of "*"
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
@limiter.limit("50/minute")
async def root(request: Request):
    return {"message": "Sturgeon AI API", "status": "online"}

@app.post("/auth/register", response_model=Token)
@limiter.limit("5/minute")  # Strict rate limit on registration
async def register(user: UserCreate, request: Request):
    # In production, save to Supabase database
    hashed = hash_password(user.password)
    access_token = create_access_token({"sub": "user_id", "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
@limiter.limit("10/minute")  # Strict rate limit on login
async def login(user: UserLogin, request: Request):
    # In production, verify against database
    access_token = create_access_token({"sub": "user_id", "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
@limiter.limit("100/minute")
async def get_user_profile(request: Request, current_user = Depends(get_current_user)):
    return current_user

@app.post("/payments/create-checkout")
@limiter.limit("20/minute")
async def create_checkout_session(request: Request, current_user = Depends(get_current_user)):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
