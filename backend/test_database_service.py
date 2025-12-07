"""
Basic tests for database_service module
"""
import pytest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def setup_test_env():
    """Set up test environment variables"""
    os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
    os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'test-key'
    yield
    # Cleanup is optional since env vars are process-scoped


def test_config_import():
    """Test config module can be imported"""
    from config import settings
    
    assert settings is not None
    assert hasattr(settings, 'supabase_url')
    assert hasattr(settings, 'supabase_service_key')
    assert hasattr(settings, 'jwt_secret')


def test_database_service_import(setup_test_env):
    """Test database_service module can be imported"""
    # This test just verifies the module has no syntax errors
    import importlib
    import sys
    
    # Remove module if already imported
    if 'database_service' in sys.modules:
        del sys.modules['database_service']
    
    try:
        # Import should not raise any exceptions
        import database_service
        assert database_service.SupabaseService is not None
        assert hasattr(database_service, 'db_service')
        assert hasattr(database_service, 'get_db_service')
    except ImportError as e:
        pytest.fail(f"Failed to import database_service: {e}")


def test_database_service_class_structure(setup_test_env):
    """Test SupabaseService class has expected methods"""
    from database_service import SupabaseService
    
    # Check that class has expected methods
    assert hasattr(SupabaseService, 'log_event')
    assert hasattr(SupabaseService, 'get_total_users')
    assert hasattr(SupabaseService, 'get_active_users')
    assert hasattr(SupabaseService, 'get_event_count')
    assert hasattr(SupabaseService, 'get_revenue_stats')
    assert hasattr(SupabaseService, 'get_top_search_terms')
    assert hasattr(SupabaseService, 'get_user_growth')
    assert hasattr(SupabaseService, 'analyze_contract')
    assert hasattr(SupabaseService, 'health_check')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
