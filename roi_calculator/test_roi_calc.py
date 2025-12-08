"""Tests for ROI Calculator module."""

import pytest
from roi_calculator import roi_calc


class TestCalculateCampaignROI:
    """Test suite for calculate_campaign_roi function."""
    
    def test_linkedin_ads_basic_calculation(self):
        """Test basic LinkedIn ads ROI calculation."""
        roi = roi_calc.calculate_campaign_roi(
            channel="linkedin_ads",
            budget=5000
        )
        
        assert roi["customers"] == 18
        assert roi["revenue"] == 42984.0
        assert roi["roi"] == 759.7
    
    def test_linkedin_ads_different_budget(self):
        """Test LinkedIn ads with different budget."""
        roi = roi_calc.calculate_campaign_roi(
            channel="linkedin_ads",
            budget=10000
        )
        
        # With double the budget, we should get approximately double the customers
        assert roi["customers"] == 36
        assert roi["revenue"] == 85968.0
        # ROI percentage should remain similar for the same channel
        assert roi["roi"] == 759.7
    
    def test_linkedin_ads_small_budget(self):
        """Test LinkedIn ads with small budget."""
        roi = roi_calc.calculate_campaign_roi(
            channel="linkedin_ads",
            budget=1000
        )
        
        assert roi["customers"] == 3
        assert roi["revenue"] == 7164.0
        assert roi["roi"] == 616.4
    
    def test_unsupported_channel_raises_error(self):
        """Test that unsupported channel raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported channel"):
            roi_calc.calculate_campaign_roi(
                channel="unsupported_channel",
                budget=5000
            )
    
    def test_return_type_structure(self):
        """Test that return value has correct structure."""
        roi = roi_calc.calculate_campaign_roi(
            channel="linkedin_ads",
            budget=5000
        )
        
        assert isinstance(roi, dict)
        assert "customers" in roi
        assert "revenue" in roi
        assert "roi" in roi
        assert isinstance(roi["customers"], int)
        assert isinstance(roi["revenue"], (int, float))
        assert isinstance(roi["roi"], (int, float))
    
    def test_roi_calculation_formula(self):
        """Test that ROI is calculated correctly using the formula."""
        roi = roi_calc.calculate_campaign_roi(
            channel="linkedin_ads",
            budget=5000
        )
        
        # ROI = ((Revenue - Budget) / Budget) * 100
        expected_roi = ((roi["revenue"] - 5000) / 5000) * 100
        assert abs(roi["roi"] - round(expected_roi, 1)) < 0.1
