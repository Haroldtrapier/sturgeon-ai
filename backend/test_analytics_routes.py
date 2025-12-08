"""
Tests for analytics API routes
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import os

# Set admin token for tests
os.environ["ADMIN_TOKEN"] = "test_admin_token_12345"

from main import app
from models import (
    HealthResponse,
    MetricsResponse,
    ContractAnalysisRequest,
    ContractAnalysisResponse,
    AnalyticsEventRequest
)

client = TestClient(app)


class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_health_check_no_auth(self):
        """Health check should work without authentication"""
        response = client.get("/api/analytics/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "timestamp" in data
        assert "version" in data
        assert "database_connected" in data
        assert "services" in data
    
    def test_status_requires_auth(self):
        """Status endpoint should require admin authentication"""
        response = client.get("/api/analytics/status")
        assert response.status_code == 401
    
    def test_status_with_valid_auth(self):
        """Status endpoint should work with valid admin token"""
        response = client.get(
            "/api/analytics/status",
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "operational"
        assert "timestamp" in data
        assert "database" in data
        assert "api" in data
        assert "analytics" in data
    
    def test_status_with_invalid_auth(self):
        """Status endpoint should reject invalid tokens"""
        response = client.get(
            "/api/analytics/status",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 403


class TestMetricsEndpoints:
    """Test analytics metrics endpoints"""
    
    def test_metrics_requires_auth(self):
        """Metrics endpoint should require authentication"""
        response = client.get("/api/analytics/metrics")
        assert response.status_code == 401
    
    def test_metrics_with_valid_auth(self):
        """Metrics endpoint should return comprehensive data"""
        response = client.get(
            "/api/analytics/metrics",
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "period" in data
        assert "total_users" in data
        assert "active_users" in data
        assert "total_searches" in data
        assert "total_contracts_analyzed" in data
        assert "total_revenue" in data
        assert "conversion_rate" in data
        assert "avg_session_duration" in data
        assert "top_search_terms" in data
        assert "user_growth" in data
        assert "revenue_by_day" in data
        assert "generated_at" in data
    
    def test_metrics_with_different_periods(self):
        """Metrics should accept different time periods"""
        periods = ["7d", "30d", "90d", "365d"]
        
        for period in periods:
            response = client.get(
                f"/api/analytics/metrics?period={period}",
                headers={"Authorization": "Bearer test_admin_token_12345"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["period"] == period
    
    def test_user_metrics_requires_auth(self):
        """User metrics endpoint should require authentication"""
        response = client.get("/api/analytics/metrics/users")
        assert response.status_code == 401
    
    def test_user_metrics_with_valid_auth(self):
        """User metrics should return detailed user statistics"""
        response = client.get(
            "/api/analytics/metrics/users",
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "total_users" in data
        assert "active_users_7d" in data
        assert "active_users_30d" in data
        assert "retention_rate_7d" in data
        assert "retention_rate_30d" in data
        assert "generated_at" in data


class TestContractAnalysisEndpoints:
    """Test contract analysis endpoints"""
    
    def test_analyze_contract_requires_auth(self):
        """Contract analysis should require authentication"""
        request_data = {
            "contract_id": "CONTRACT-001",
            "user_id": "user-123"
        }
        response = client.post(
            "/api/analytics/analyze-contract",
            json=request_data
        )
        assert response.status_code == 401
    
    def test_analyze_contract_with_valid_auth(self):
        """Contract analysis should return detailed results"""
        request_data = {
            "contract_id": "CONTRACT-001",
            "user_id": "user-123",
            "contract_type": "GSA Schedule",
            "metadata": {"value": 1000000}
        }
        response = client.post(
            "/api/analytics/analyze-contract",
            json=request_data,
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["contract_id"] == "CONTRACT-001"
        assert "analysis_id" in data
        assert "risk_score" in data
        assert "opportunities" in data
        assert "compliance_status" in data
        assert "recommendations" in data
        assert "analyzed_at" in data
    
    def test_contract_stats_requires_auth(self):
        """Contract stats should require authentication"""
        response = client.get("/api/analytics/contracts/stats")
        assert response.status_code == 401
    
    def test_contract_stats_with_valid_auth(self):
        """Contract stats should return aggregate data"""
        response = client.get(
            "/api/analytics/contracts/stats?days=30",
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "period_days" in data
        assert "total_analyses" in data
        assert "avg_per_day" in data
        assert "generated_at" in data


class TestEventLoggingEndpoints:
    """Test event logging endpoints"""
    
    def test_log_event_requires_auth(self):
        """Event logging should require authentication"""
        event_data = {
            "event_type": "search",
            "user_id": "user-123",
            "session_id": "session-456",
            "metadata": {"query": "federal contracts"}
        }
        response = client.post(
            "/api/analytics/events",
            json=event_data
        )
        assert response.status_code == 401
    
    def test_log_event_with_valid_auth(self):
        """Event logging should record events"""
        event_data = {
            "event_type": "search",
            "user_id": "user-123",
            "session_id": "session-456",
            "metadata": {"query": "federal contracts"}
        }
        response = client.post(
            "/api/analytics/events",
            json=event_data,
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "event_id" in data
        assert "timestamp" in data
        assert data["event_type"] == "search"


class TestSearchAnalyticsEndpoints:
    """Test search analytics endpoints"""
    
    def test_top_search_terms_requires_auth(self):
        """Top search terms should require authentication"""
        response = client.get("/api/analytics/searches/top-terms")
        assert response.status_code == 401
    
    def test_top_search_terms_with_valid_auth(self):
        """Top search terms should return popular searches"""
        response = client.get(
            "/api/analytics/searches/top-terms?limit=10",
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "top_terms" in data
        assert "total_terms" in data
        assert "generated_at" in data
        assert len(data["top_terms"]) <= 10
    
    def test_top_search_terms_custom_limit(self):
        """Top search terms should respect custom limit"""
        response = client.get(
            "/api/analytics/searches/top-terms?limit=5",
            headers={"Authorization": "Bearer test_admin_token_12345"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["top_terms"]) <= 5


class TestAuthenticationMechanisms:
    """Test authentication and authorization"""
    
    def test_missing_authorization_header(self):
        """Endpoints should reject requests without auth header"""
        response = client.get("/api/analytics/metrics")
        assert response.status_code == 401
    
    def test_malformed_authorization_header(self):
        """Endpoints should reject malformed auth headers"""
        # Missing "Bearer" prefix
        response = client.get(
            "/api/analytics/metrics",
            headers={"Authorization": "test_admin_token_12345"}
        )
        assert response.status_code == 401
    
    def test_wrong_token(self):
        """Endpoints should reject invalid tokens"""
        response = client.get(
            "/api/analytics/metrics",
            headers={"Authorization": "Bearer wrong_token"}
        )
        assert response.status_code == 403


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
