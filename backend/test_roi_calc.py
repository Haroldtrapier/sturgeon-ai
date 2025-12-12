"""
backend/test_roi_calc.py
Tests for ROI Calculator
"""

import pytest
from roi_calc import ROICalculator, optimize_budget_allocation


class TestROICalculator:
    """Test suite for ROICalculator class"""
    
    def test_optimize_budget_allocation_basic(self):
        """Test basic budget allocation with default weights"""
        roi_calc = ROICalculator()
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=10000,
            channels=["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        # Verify the optimal split: 60% LinkedIn / 30% Content / 10% Email
        assert abs(allocation["linkedin_ads"] - 6000.0) < 0.01
        assert abs(allocation["content_marketing"] - 3000.0) < 0.01
        assert abs(allocation["email_marketing"] - 1000.0) < 0.01
        
        # Verify total equals budget
        assert abs(sum(allocation.values()) - 10000.0) < 0.01
    
    def test_optimize_budget_allocation_different_order(self):
        """Test that channel order doesn't affect allocation"""
        roi_calc = ROICalculator()
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=10000,
            channels=["email_marketing", "linkedin_ads", "content_marketing"]
        )
        
        assert abs(allocation["linkedin_ads"] - 6000.0) < 0.01
        assert abs(allocation["content_marketing"] - 3000.0) < 0.01
        assert abs(allocation["email_marketing"] - 1000.0) < 0.01
    
    def test_optimize_budget_allocation_subset_channels(self):
        """Test allocation with subset of channels"""
        roi_calc = ROICalculator()
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=10000,
            channels=["linkedin_ads", "content_marketing"]
        )
        
        # Should allocate based on relative weights (60:30 ratio becomes 2:1)
        expected_linkedin = 10000 * (0.60 / 0.90)  # ~6666.67
        expected_content = 10000 * (0.30 / 0.90)   # ~3333.33
        
        assert abs(allocation["linkedin_ads"] - expected_linkedin) < 0.01
        assert abs(allocation["content_marketing"] - expected_content) < 0.01
        assert abs(sum(allocation.values()) - 10000.0) < 0.01
    
    def test_optimize_budget_allocation_single_channel(self):
        """Test allocation with single channel"""
        roi_calc = ROICalculator()
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=5000,
            channels=["linkedin_ads"]
        )
        
        assert allocation["linkedin_ads"] == 5000.0
        assert len(allocation) == 1
    
    def test_optimize_budget_allocation_custom_weights(self):
        """Test allocation with custom weights"""
        roi_calc = ROICalculator()
        custom_weights = {
            "linkedin_ads": 0.50,
            "content_marketing": 0.30,
            "email_marketing": 0.20
        }
        
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=10000,
            channels=["linkedin_ads", "content_marketing", "email_marketing"],
            custom_weights=custom_weights
        )
        
        assert abs(allocation["linkedin_ads"] - 5000.0) < 0.01
        assert abs(allocation["content_marketing"] - 3000.0) < 0.01
        assert abs(allocation["email_marketing"] - 2000.0) < 0.01
    
    def test_optimize_budget_allocation_unknown_channel(self):
        """Test allocation with unknown channel gets equal distribution"""
        roi_calc = ROICalculator()
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=10000,
            channels=["unknown_channel"]
        )
        
        # Unknown channel should get full budget
        assert allocation["unknown_channel"] == 10000.0
    
    def test_optimize_budget_allocation_mixed_channels(self):
        """Test allocation with mix of known and unknown channels"""
        roi_calc = ROICalculator()
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=10000,
            channels=["linkedin_ads", "unknown_channel"]
        )
        
        # Should only allocate to known channel
        assert allocation["linkedin_ads"] == 10000.0
        assert allocation["unknown_channel"] == 0.0
    
    def test_optimize_budget_allocation_invalid_budget(self):
        """Test that negative budget raises error"""
        roi_calc = ROICalculator()
        
        with pytest.raises(ValueError, match="Total budget must be positive"):
            roi_calc.optimize_budget_allocation(
                total_budget=-1000,
                channels=["linkedin_ads"]
            )
        
        with pytest.raises(ValueError, match="Total budget must be positive"):
            roi_calc.optimize_budget_allocation(
                total_budget=0,
                channels=["linkedin_ads"]
            )
    
    def test_optimize_budget_allocation_empty_channels(self):
        """Test that empty channels list raises error"""
        roi_calc = ROICalculator()
        
        with pytest.raises(ValueError, match="At least one channel must be specified"):
            roi_calc.optimize_budget_allocation(
                total_budget=10000,
                channels=[]
            )
    
    def test_set_allocation_strategy(self):
        """Test setting custom allocation strategy"""
        roi_calc = ROICalculator()
        
        new_strategy = {
            "linkedin_ads": 0.40,
            "content_marketing": 0.35,
            "email_marketing": 0.25
        }
        
        roi_calc.set_allocation_strategy(new_strategy)
        
        allocation = roi_calc.optimize_budget_allocation(
            total_budget=10000,
            channels=["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        assert abs(allocation["linkedin_ads"] - 4000.0) < 0.01
        assert abs(allocation["content_marketing"] - 3500.0) < 0.01
        assert abs(allocation["email_marketing"] - 2500.0) < 0.01
    
    def test_set_allocation_strategy_invalid_sum(self):
        """Test that invalid strategy sum raises error"""
        roi_calc = ROICalculator()
        
        invalid_strategy = {
            "linkedin_ads": 0.50,
            "content_marketing": 0.30,
            "email_marketing": 0.10  # Sums to 0.90, not 1.0
        }
        
        with pytest.raises(ValueError, match="must sum to 1.0"):
            roi_calc.set_allocation_strategy(invalid_strategy)
    
    def test_calculate_roi(self):
        """Test ROI calculation"""
        roi_calc = ROICalculator()
        
        # Investment of 1000, revenue of 1500 = 50% ROI
        roi = roi_calc.calculate_roi(
            channel="linkedin_ads",
            investment=1000,
            revenue=1500
        )
        
        assert roi == 50.0
    
    def test_calculate_roi_zero_investment(self):
        """Test ROI with zero investment"""
        roi_calc = ROICalculator()
        
        roi = roi_calc.calculate_roi(
            channel="linkedin_ads",
            investment=0,
            revenue=1000
        )
        
        assert roi == 0.0
    
    def test_calculate_roi_negative_return(self):
        """Test ROI with loss"""
        roi_calc = ROICalculator()
        
        # Investment of 1000, revenue of 800 = -20% ROI
        roi = roi_calc.calculate_roi(
            channel="linkedin_ads",
            investment=1000,
            revenue=800
        )
        
        assert roi == -20.0
    
    def test_get_channel_performance(self):
        """Test channel performance projection"""
        roi_calc = ROICalculator()
        
        allocations = {
            "linkedin_ads": 6000.0,
            "content_marketing": 3000.0,
            "email_marketing": 1000.0
        }
        
        historical_roi = {
            "linkedin_ads": 150.0,      # 150% ROI
            "content_marketing": 200.0,  # 200% ROI
            "email_marketing": 100.0     # 100% ROI
        }
        
        performance = roi_calc.get_channel_performance(allocations, historical_roi)
        
        # LinkedIn: 6000 * 2.5 = 15000 revenue, 9000 profit
        assert performance["linkedin_ads"]["investment"] == 6000.0
        assert performance["linkedin_ads"]["roi_percentage"] == 150.0
        assert performance["linkedin_ads"]["projected_revenue"] == 15000.0
        assert performance["linkedin_ads"]["projected_profit"] == 9000.0
        
        # Content: 3000 * 3 = 9000 revenue, 6000 profit
        assert performance["content_marketing"]["investment"] == 3000.0
        assert performance["content_marketing"]["roi_percentage"] == 200.0
        assert performance["content_marketing"]["projected_revenue"] == 9000.0
        assert performance["content_marketing"]["projected_profit"] == 6000.0
        
        # Email: 1000 * 2 = 2000 revenue, 1000 profit
        assert performance["email_marketing"]["investment"] == 1000.0
        assert performance["email_marketing"]["roi_percentage"] == 100.0
        assert performance["email_marketing"]["projected_revenue"] == 2000.0
        assert performance["email_marketing"]["projected_profit"] == 1000.0
    
    def test_get_channel_performance_no_historical_data(self):
        """Test performance projection with no historical data"""
        roi_calc = ROICalculator()
        
        allocations = {
            "new_channel": 5000.0
        }
        
        historical_roi = {}
        
        performance = roi_calc.get_channel_performance(allocations, historical_roi)
        
        # Should assume 0% ROI for unknown channel
        assert performance["new_channel"]["investment"] == 5000.0
        assert performance["new_channel"]["roi_percentage"] == 0.0
        assert performance["new_channel"]["projected_revenue"] == 5000.0
        assert performance["new_channel"]["projected_profit"] == 0.0


class TestConvenienceFunction:
    """Test module-level convenience function"""
    
    def test_optimize_budget_allocation_convenience(self):
        """Test convenience function works correctly"""
        allocation = optimize_budget_allocation(
            total_budget=10000,
            channels=["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        # Optimal split: 60% LinkedIn / 30% Content / 10% Email
        assert abs(allocation["linkedin_ads"] - 6000.0) < 0.01
        assert abs(allocation["content_marketing"] - 3000.0) < 0.01
        assert abs(allocation["email_marketing"] - 1000.0) < 0.01
    
    def test_optimize_budget_allocation_convenience_custom_weights(self):
        """Test convenience function with custom weights"""
        custom_weights = {
            "linkedin_ads": 0.70,
            "content_marketing": 0.20,
            "email_marketing": 0.10
        }
        
        allocation = optimize_budget_allocation(
            total_budget=10000,
            channels=["linkedin_ads", "content_marketing", "email_marketing"],
            custom_weights=custom_weights
        )
        
        assert abs(allocation["linkedin_ads"] - 7000.0) < 0.01
        assert abs(allocation["content_marketing"] - 2000.0) < 0.01
        assert abs(allocation["email_marketing"] - 1000.0) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
