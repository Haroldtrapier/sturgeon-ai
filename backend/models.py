"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    database_connected: bool
    services: Dict[str, str]


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
    user_growth: Dict[str, Any]
    revenue_by_day: List[Dict[str, Any]]
    generated_at: datetime


class ContractAnalysisRequest(BaseModel):
    """Request model for contract analysis"""
    contract_id: str = Field(..., description="Unique contract identifier")
    user_id: str = Field(..., description="User requesting the analysis")
    contract_type: Optional[str] = Field(None, description="Type of contract")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class ContractAnalysisResponse(BaseModel):
    """Response model for contract analysis"""
    contract_id: str
    analysis_id: str
    risk_score: float
    opportunities: List[Dict[str, Any]]
    compliance_status: str
    recommendations: List[str]
    analyzed_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class AnalyticsEventRequest(BaseModel):
    """Request model for logging analytics events"""
    event_type: str = Field(..., description="Type of event (e.g., 'search', 'contract_analysis')")
    user_id: Optional[str] = Field(None, description="User ID associated with the event")
    session_id: Optional[str] = Field(None, description="Session ID for the event")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Event metadata")
