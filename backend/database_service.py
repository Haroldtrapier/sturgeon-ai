"""
Sturgeon AI Analytics Dashboard - Database Service
Supabase integration for analytics data management
"""

from supabase import create_client, Client
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from config import settings
import structlog

logger = structlog.get_logger()


class SupabaseService:
    """Service class for Supabase database operations"""
    
    def __init__(self):
        """Initialize Supabase client"""
        # Check if credentials are properly configured (not placeholders)
        if (not settings.supabase_url or 
            not settings.supabase_service_key or 
            "your_supabase" in settings.supabase_url.lower() or
            "your_supabase" in settings.supabase_service_key.lower()):
            logger.warning("Supabase credentials not configured. Service will be limited.")
            self.client: Optional[Client] = None
        else:
            try:
                self.client: Client = create_client(
                    settings.supabase_url,
                    settings.supabase_service_key
                )
            except Exception as e:
                logger.error("Failed to initialize Supabase client", error=str(e))
                self.client: Optional[Client] = None
        
    def _ensure_client(self):
        """Ensure client is initialized"""
        if self.client is None:
            raise RuntimeError("Supabase client not initialized. Check configuration.")
    
    async def log_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Log an analytics event"""
        self._ensure_client()
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
        self._ensure_client()
        try:
            result = self.client.table("users").select("id", count="exact").execute()
            return result.count or 0
        except Exception as e:
            logger.error("failed_to_get_total_users", error=str(e))
            return 0
    
    async def get_active_users(self, days: int = 30) -> int:
        """Get count of users active in the last N days"""
        self._ensure_client()
        try:
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            result = (
                self.client.table("analytics_events")
                .select("user_id", count="exact")
                .gte("timestamp", cutoff_date)
                .not_.is_("user_id", "null")
                .execute()
            )
            
            # Count unique user_ids
            unique_users = len(set(event["user_id"] for event in result.data if event.get("user_id")))
            return unique_users
            
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
        self._ensure_client()
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
        self._ensure_client()
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
        self._ensure_client()
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
        self._ensure_client()
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
        self._ensure_client()
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
            import random
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
            
            # Store analysis results
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
        if self.client is None:
            return False
        try:
            # Simple query to verify connection
            self.client.table("analytics_events").select("id").limit(1).execute()
            return True
        except Exception as e:
            logger.error("health_check_failed", error=str(e))
            return False


# Global service instance
db_service = SupabaseService()
