"""
Sturgeon AI Analytics Dashboard - API Routes
Real-time operational metrics and business intelligence tracking
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Optional
import structlog

from models import (
    HealthResponse,
    MetricsResponse,
    ContractAnalysisRequest,
    ContractAnalysisResponse,
    AnalyticsEventRequest
)
from database import db_service
from auth import verify_admin_token
from config import settings

logger = structlog.get_logger()

# Initialize router
analytics_router = APIRouter(prefix="/api/analytics", tags=["analytics"])


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@analytics_router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    System health check endpoint
    
    Returns service status, database connectivity, and version info
    No authentication required - public endpoint
    """
    try:
        db_connected = await db_service.health_check()
        
        return HealthResponse(
            status="healthy" if db_connected else "degraded",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database_connected=db_connected,
            services={
                "api": "operational",
                "database": "operational" if db_connected else "unavailable",
                "analytics": "operational"
            }
        )
    except Exception as e:
        logger.error("health_check_failed", error=str(e))
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database_connected=False,
            services={
                "api": "degraded",
                "database": "unavailable",
                "analytics": "degraded"
            }
        )


@analytics_router.get("/status")
async def get_status(
    authorization: Optional[str] = Header(None)
):
    """
    Detailed system status endpoint
    
    Requires admin authentication
    Returns comprehensive system metrics and health indicators
    """
    await verify_admin_token(authorization)
    
    try:
        # Gather system metrics
        db_connected = await db_service.health_check()
        
        return {
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": "calculating...",
            "database": {
                "connected": db_connected,
                "pool_size": "N/A",
                "active_connections": 0
            },
            "api": {
                "version": "1.0.0",
                "environment": settings.environment,
                "debug_mode": settings.debug
            },
            "analytics": {
                "events_processed_today": "calculating...",
                "error_rate": 0.0
            }
        }
    except Exception as e:
        logger.error("status_check_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve system status")


# ============================================================================
# ANALYTICS METRICS ENDPOINTS
# ============================================================================

@analytics_router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    period: str = "30d",
    authorization: Optional[str] = Header(None)
):
    """
    Comprehensive analytics metrics dashboard
    
    Args:
        period: Time period for metrics (7d, 30d, 90d, 365d)
        
    Returns:
        Aggregated business intelligence metrics including:
        - User statistics (total, active, growth)
        - Search metrics
        - Contract analysis metrics
        - Revenue data
        - Conversion rates
        - Top performing searches
        
    Requires admin authentication
    """
    await verify_admin_token(authorization)
    
    try:
        # Parse period
        period_days = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "365d": 365
        }.get(period, 30)
        
        start_date = datetime.utcnow() - timedelta(days=period_days)
        end_date = datetime.utcnow()
        
        # Gather all metrics in parallel
        total_users = await db_service.get_total_users()
        active_users = await db_service.get_active_users(days=period_days)
        
        total_searches = await db_service.get_event_count(
            "search",
            start_date=start_date,
            end_date=end_date
        )
        
        total_contracts = await db_service.get_event_count(
            "contract_analysis",
            start_date=start_date,
            end_date=end_date
        )
        
        revenue_stats = await db_service.get_revenue_stats(
            start_date=start_date,
            end_date=end_date
        )
        
        top_searches = await db_service.get_top_search_terms(limit=10)
        user_growth = await db_service.get_user_growth(days=period_days)
        
        # Calculate conversion rate
        total_registrations = await db_service.get_event_count(
            "user_registration",
            start_date=start_date,
            end_date=end_date
        )
        
        # Calculate conversion rate with safe division
        if total_registrations > 0:
            conversion_rate = revenue_stats["transaction_count"] / total_registrations * 100
        else:
            conversion_rate = 0.0
        
        # Calculate average session duration (simulated for now)
        avg_session_duration = 8.5  # minutes - replace with actual calculation
        
        # Format revenue by day (simulated for now)
        revenue_by_day = [
            {
                "date": (end_date - timedelta(days=i)).strftime("%Y-%m-%d"),
                "revenue": revenue_stats["total_revenue"] / period_days if period_days > 0 else 0
            }
            for i in range(min(period_days, 30))
        ]
        
        return MetricsResponse(
            period=period,
            total_users=total_users,
            active_users=active_users,
            total_searches=total_searches,
            total_contracts_analyzed=total_contracts,
            total_revenue=revenue_stats["total_revenue"],
            conversion_rate=round(conversion_rate, 2),
            avg_session_duration=avg_session_duration,
            top_search_terms=top_searches,
            user_growth=user_growth,
            revenue_by_day=revenue_by_day[::-1],  # Reverse for chronological order
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("failed_to_get_metrics", error=str(e), period=period)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve metrics: {str(e)}"
        )


@analytics_router.get("/metrics/users")
async def get_user_metrics(
    authorization: Optional[str] = Header(None)
):
    """
    Detailed user analytics
    
    Returns comprehensive user behavior metrics
    Requires admin authentication
    """
    await verify_admin_token(authorization)
    
    try:
        total_users = await db_service.get_total_users()
        active_7d = await db_service.get_active_users(days=7)
        active_30d = await db_service.get_active_users(days=30)
        
        return {
            "total_users": total_users,
            "active_users_7d": active_7d,
            "active_users_30d": active_30d,
            "retention_rate_7d": round(active_7d / total_users * 100, 2) if total_users > 0 else 0,
            "retention_rate_30d": round(active_30d / total_users * 100, 2) if total_users > 0 else 0,
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("failed_to_get_user_metrics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve user metrics")


# ============================================================================
# CONTRACT ANALYSIS ENDPOINTS
# ============================================================================

@analytics_router.post("/analyze-contract", response_model=ContractAnalysisResponse)
async def analyze_contract(
    request: ContractAnalysisRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Analyze a government contract
    
    Args:
        request: Contract analysis parameters
        
    Returns:
        Detailed analysis including risk factors, opportunities, and compliance
        
    Requires admin authentication
    """
    await verify_admin_token(authorization)
    
    try:
        logger.info(
            "contract_analysis_requested",
            contract_id=request.contract_id,
            user_id=request.user_id,
            contract_type=request.contract_type
        )
        
        # Perform contract analysis
        result = await db_service.analyze_contract(
            contract_id=request.contract_id,
            user_id=request.user_id,
            contract_type=request.contract_type,
            metadata=request.metadata
        )
        
        return ContractAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(
            "contract_analysis_failed",
            error=str(e),
            contract_id=request.contract_id
        )
        raise HTTPException(
            status_code=500,
            detail=f"Contract analysis failed: {str(e)}"
        )


@analytics_router.get("/contracts/stats")
async def get_contract_stats(
    days: int = 30,
    authorization: Optional[str] = Header(None)
):
    """
    Contract analysis statistics
    
    Returns aggregate statistics about contract analyses
    Requires admin authentication
    """
    await verify_admin_token(authorization)
    
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        total_analyses = await db_service.get_event_count(
            "contract_analysis",
            start_date=start_date
        )
        
        return {
            "period_days": days,
            "total_analyses": total_analyses,
            "avg_per_day": round(total_analyses / days, 2) if days > 0 else 0,
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("failed_to_get_contract_stats", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve contract statistics")


# ============================================================================
# EVENT LOGGING ENDPOINTS
# ============================================================================

@analytics_router.post("/events")
async def log_event(
    event: AnalyticsEventRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Log an analytics event
    
    Args:
        event: Event data to log
        
    Returns:
        Event confirmation with assigned ID
        
    Requires admin authentication for manual event logging
    """
    await verify_admin_token(authorization)
    
    try:
        result = await db_service.log_event(
            event_type=event.event_type,
            user_id=event.user_id,
            session_id=event.session_id,
            metadata=event.metadata
        )
        
        return {
            "status": "success",
            "event_id": result.get("id"),
            "timestamp": result.get("timestamp"),
            "event_type": event.event_type
        }
    except Exception as e:
        logger.error("failed_to_log_event", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to log event: {str(e)}")


# ============================================================================
# SEARCH ANALYTICS ENDPOINTS
# ============================================================================

@analytics_router.get("/searches/top-terms")
async def get_top_search_terms(
    limit: int = 20,
    authorization: Optional[str] = Header(None)
):
    """
    Get most popular search terms
    
    Args:
        limit: Number of top terms to return
        
    Returns:
        List of search terms with frequency counts
        
    Requires admin authentication
    """
    await verify_admin_token(authorization)
    
    try:
        top_terms = await db_service.get_top_search_terms(limit=limit)
        
        return {
            "top_terms": top_terms,
            "total_terms": len(top_terms),
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("failed_to_get_top_terms", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve search terms")


# Export router
__all__ = ["analytics_router"]
