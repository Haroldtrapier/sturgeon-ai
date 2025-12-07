"""
Sturgeon AI Analytics Dashboard - Database Service
Supabase integration for analytics data management
"""

from supabase import create_client, Client
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from config import settings
import structlog
import random

logger = structlog.get_logger()


class SupabaseService:
    """Service class for Supabase database operations"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key
        )
        
    async def log_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Log an analytics event"""
        try:
            event_data = {
                "event_type": event_type,
                "user_id": user_id,
                "session_id": session_id,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat()
            }
            
            result = self.client.table("analytics_events").insert(event_data).execute()
            logger.info("event_logged", event_type=event_type, user_id=user_id)
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error("failed_to_log_event", error=str(e), event_type=event_type)
            raise
    
    async def get_total_users(self) -> int:
        """Get total registered users count"""
        try:
            result = self.client.table("users").select("id", count="exact").execute()
            return result.count or 0
        except Exception as e:
            logger.error("failed_to_get_total_users", error=str(e))
            return 0
    
    async def get_active_users(self, days: int = 30) -> int:
        """Get count of users active in the last N days"""
        try:
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            # Use PostgreSQL to count distinct users for better performance
            result = (
                self.client.rpc('count_distinct_active_users', {
                    'cutoff_timestamp': cutoff_date
                }).execute()
            )
            
            # Fallback to Python-based counting if RPC function doesn't exist
            if result.data is None:
                result = (
                    self.client.table("analytics_events")
                    .select("user_id")
                    .gte("timestamp", cutoff_date)
                    .not_.is_("user_id", "null")
                    .execute()
                )
                unique_users = len(set(event["user_id"] for event in result.data if event.get("user_id")))
                return unique_users
            
            return result.data if isinstance(result.data, int) else 0
            
        except Exception as e:
            logger.error("failed_to_get_active_users", error=str(e))
            return 0
    
    async def get_event_count(
        self,
        event_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """Get count of events by type within date range"""
        try:
            query = self.client.table("analytics_events").select("id", count="exact").eq("event_type", event_type)
            
            if start_date:
                query = query.gte("timestamp", start_date.isoformat())
            if end_date:
                query = query.lte("timestamp", end_date.isoformat())
            
            result = query.execute()
            return result.count or 0
            
        except Exception as e:
            logger.error("failed_to_get_event_count", error=str(e), event_type=event_type)
            return 0
    
    async def get_revenue_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get revenue statistics"""
        try:
            query = self.client.table("analytics_events").select("metadata").eq("event_type", "payment")
            
            if start_date:
                query = query.gte("timestamp", start_date.isoformat())
            if end_date:
                query = query.lte("timestamp", end_date.isoformat())
            
            result = query.execute()
            
            total_revenue = sum(
                event.get("metadata", {}).get("amount", 0)
                for event in result.data
            )
            
            return {
                "total_revenue": total_revenue,
                "transaction_count": len(result.data),
                "average_transaction": total_revenue / len(result.data) if result.data else 0
            }
            
        except Exception as e:
            logger.error("failed_to_get_revenue_stats", error=str(e))
            return {"total_revenue": 0, "transaction_count": 0, "average_transaction": 0}
    
    async def get_top_search_terms(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular search terms"""
        try:
            result = (
                self.client.table("analytics_events")
                .select("metadata")
                .eq("event_type", "search")
                .limit(1000)
                .execute()
            )
            
            # Aggregate search terms
            search_counts: Dict[str, int] = {}
            for event in result.data:
                term = event.get("metadata", {}).get("search_term", "").lower().strip()
                if term:
                    search_counts[term] = search_counts.get(term, 0) + 1
            
            # Sort and format
            top_terms = sorted(
                [{"term": term, "count": count} for term, count in search_counts.items()],
                key=lambda x: x["count"],
                reverse=True
            )[:limit]
            
            return top_terms
            
        except Exception as e:
            logger.error("failed_to_get_top_search_terms", error=str(e))
            return []
    
    async def get_user_growth(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get daily user registration counts"""
        try:
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            result = (
                self.client.table("analytics_events")
                .select("timestamp")
                .eq("event_type", "user_registration")
                .gte("timestamp", cutoff_date)
                .order("timestamp")
                .execute()
            )
            
            # Aggregate by date
            daily_counts: Dict[str, int] = {}
            for event in result.data:
                date_key = event["timestamp"][:10]  # Extract YYYY-MM-DD
                daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
            
            # Format output
            growth_data = [
                {"date": date, "count": count}
                for date, count in sorted(daily_counts.items())
            ]
            
            return growth_data
            
        except Exception as e:
            logger.error("failed_to_get_user_growth", error=str(e))
            return []
    
    async def analyze_contract(
        self,
        contract_id: str,
        user_id: str,
        contract_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze a contract and return insights"""
        start_time = datetime.utcnow()
        
        try:
            # Log the analysis request
            await self.log_event(
                event_type="contract_analysis",
                user_id=user_id,
                metadata={
                    "contract_id": contract_id,
                    "contract_type": contract_type,
                    **(metadata or {})
                }
            )
            
            # Simulate contract analysis (replace with actual AI analysis)
            analysis_score = random.uniform(0.6, 0.95)
            
            risk_factors = [
                "Non-standard payment terms",
                "Unclear termination clause",
                "Missing liability limitations"
            ] if analysis_score < 0.8 else ["No significant risks identified"]
            
            opportunities = [
                "Potential for cost reduction",
                "Favorable renewal terms available",
                "Strategic partnership potential"
            ]
            
            processing_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            result = {
                "contract_id": contract_id,
                "status": "completed",
                "analysis_score": round(analysis_score, 2),
                "risk_factors": risk_factors,
                "opportunities": opportunities[:2],
                "compliance_status": "compliant" if analysis_score > 0.75 else "review_required",
                "processing_time_ms": processing_time,
                "completed_at": datetime.utcnow().isoformat()
            }
            
            # Store analysis results (Supabase client operations are synchronous)
            self.client.table("contract_analyses").insert({
                "contract_id": contract_id,
                "user_id": user_id,
                "results": result,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            
            return result
            
        except Exception as e:
            logger.error("failed_to_analyze_contract", error=str(e), contract_id=contract_id)
            raise
    
    async def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            # Simple query to verify connection
            self.client.table("analytics_events").select("id").limit(1).execute()
            return True
        except Exception as e:
            logger.error("health_check_failed", error=str(e))
            return False


# Global service instance - lazy initialization
_db_service = None


def get_db_service() -> SupabaseService:
    """Get or create the global database service instance"""
    global _db_service
    if _db_service is None:
        _db_service = SupabaseService()
    return _db_service


# For backwards compatibility
db_service = None  # Will be set on first import if settings are available
try:
    if settings.supabase_url and settings.supabase_service_key:
        db_service = SupabaseService()
except Exception:
    # Allow module import even if Supabase is not configured
    pass
