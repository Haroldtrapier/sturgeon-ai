"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List


# ============================================================================
# HEALTH & STATUS MODELS
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    database_connected: bool
    services: Dict[str, str]


# ============================================================================
# ANALYTICS MODELS
# ============================================================================

class MetricsResponse(BaseModel):
    """Comprehensive analytics metrics response"""
    period: str
    total_users: int
    active_users: int
    total_searches: int
    total_contracts_analyzed: int
    total_revenue: float
    conversion_rate: float
    avg_session_duration: float
    top_search_terms: List[Dict[str, Any]]
    user_growth: List[Dict[str, Any]]
    revenue_by_day: List[Dict[str, Any]]
    generated_at: datetime


# ============================================================================
# CONTRACT ANALYSIS MODELS
# ============================================================================

class ContractAnalysisRequest(BaseModel):
    """Contract analysis request model"""
    contract_id: str
    user_id: str
    contract_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ContractAnalysisResponse(BaseModel):
    """Contract analysis response model"""
    contract_id: str
    analysis_id: str
    risk_score: float = Field(..., ge=0, le=100)
    opportunities: List[str]
    compliance_issues: List[str]
    recommendations: List[str]
    estimated_value: Optional[float] = None
    analyzed_at: datetime


# ============================================================================
# EVENT LOGGING MODELS
# ============================================================================

class AnalyticsEventRequest(BaseModel):
    """Analytics event logging request"""
    event_type: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
