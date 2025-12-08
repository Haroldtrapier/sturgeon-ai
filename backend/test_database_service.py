"""
Tests for database_service.py

Note: These tests require a properly configured Supabase instance.
They demonstrate the API usage and verify imports work correctly.
"""

import pytest
import sys
from datetime import datetime, timedelta

# Ensure the backend module is in the path
sys.path.insert(0, '.')

from database_service import SupabaseService, db_service, MAX_SEARCH_EVENTS_TO_ANALYZE
from config import settings


class TestSupabaseServiceImports:
    """Test that the service can be imported and initialized"""
    
    def test_import_service_class(self):
        """Test that SupabaseService class can be imported"""
        assert SupabaseService is not None
        
    def test_import_global_instance(self):
        """Test that db_service global instance exists"""
        assert db_service is not None
        assert isinstance(db_service, SupabaseService)
    
    def test_constants_defined(self):
        """Test that module constants are defined"""
        assert MAX_SEARCH_EVENTS_TO_ANALYZE == 1000


class TestSupabaseServiceMethods:
    """Test that service methods are defined with correct signatures"""
    
    def test_has_log_event_method(self):
        """Test log_event method exists"""
        assert hasattr(db_service, 'log_event')
        assert callable(getattr(db_service, 'log_event'))
    
    def test_has_get_total_users_method(self):
        """Test get_total_users method exists"""
        assert hasattr(db_service, 'get_total_users')
        assert callable(getattr(db_service, 'get_total_users'))
    
    def test_has_get_active_users_method(self):
        """Test get_active_users method exists"""
        assert hasattr(db_service, 'get_active_users')
        assert callable(getattr(db_service, 'get_active_users'))
    
    def test_has_get_event_count_method(self):
        """Test get_event_count method exists"""
        assert hasattr(db_service, 'get_event_count')
        assert callable(getattr(db_service, 'get_event_count'))
    
    def test_has_get_revenue_stats_method(self):
        """Test get_revenue_stats method exists"""
        assert hasattr(db_service, 'get_revenue_stats')
        assert callable(getattr(db_service, 'get_revenue_stats'))
    
    def test_has_get_top_search_terms_method(self):
        """Test get_top_search_terms method exists"""
        assert hasattr(db_service, 'get_top_search_terms')
        assert callable(getattr(db_service, 'get_top_search_terms'))
    
    def test_has_get_user_growth_method(self):
        """Test get_user_growth method exists"""
        assert hasattr(db_service, 'get_user_growth')
        assert callable(getattr(db_service, 'get_user_growth'))
    
    def test_has_analyze_contract_method(self):
        """Test analyze_contract method exists"""
        assert hasattr(db_service, 'analyze_contract')
        assert callable(getattr(db_service, 'analyze_contract'))
    
    def test_has_health_check_method(self):
        """Test health_check method exists"""
        assert hasattr(db_service, 'health_check')
        assert callable(getattr(db_service, 'health_check'))


class TestConfigSettings:
    """Test that configuration is loaded correctly"""
    
    def test_settings_has_supabase_url(self):
        """Test that settings has supabase_url"""
        assert hasattr(settings, 'supabase_url')
    
    def test_settings_has_supabase_service_key(self):
        """Test that settings has supabase_service_key"""
        assert hasattr(settings, 'supabase_service_key')
    
    def test_settings_has_environment(self):
        """Test that settings has environment"""
        assert hasattr(settings, 'environment')
        assert settings.environment in ['development', 'production', 'staging']


# Integration tests would go here
# These would require actual Supabase credentials and are skipped in CI
@pytest.mark.skip(reason="Requires configured Supabase instance")
class TestSupabaseServiceIntegration:
    """Integration tests that require a real Supabase connection"""
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test database health check"""
        # This would fail without proper credentials
        result = await db_service.health_check()
        assert isinstance(result, bool)
    
    @pytest.mark.asyncio
    async def test_log_event(self):
        """Test logging an analytics event"""
        result = await db_service.log_event(
            event_type="test_event",
            user_id="test_user",
            metadata={"test": "data"}
        )
        assert isinstance(result, dict)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
