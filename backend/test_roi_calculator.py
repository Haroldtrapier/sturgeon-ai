"""
Tests for roi_calculator module
"""

import pytest
from roi_calculator import roi_calc, ROICalculator, ROIResult, BudgetAllocation


class TestROICalculator:
    """Test cases for ROICalculator class"""
    
    def test_calculate_campaign_roi_linkedin_ads(self):
        """Test ROI calculation for LinkedIn ads"""
        result = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)
        
        # Verify result structure
        assert isinstance(result, ROIResult)
        assert result.channel == "linkedin_ads"
        assert result.budget == 5000
        
        # Verify calculations
        assert result.expected_customers > 0
        assert result.expected_revenue > 0
        assert result.roi_percentage > 0
        assert result.cost_per_customer > 0
        assert result.revenue_per_customer > 0
        
        # For $5000 budget, should get around 18 customers
        assert 15 <= result.expected_customers <= 25
        
        # Revenue should be significant
        assert result.expected_revenue > 30000
        
        # ROI should be positive and substantial
        assert result.roi_percentage > 500
    
    def test_calculate_campaign_roi_different_channels(self):
        """Test ROI calculation for different marketing channels"""
        channels = ["linkedin_ads", "content_marketing", "email_marketing", 
                   "google_ads", "seo", "webinars"]
        budget = 3000
        
        for channel in channels:
            result = roi_calc.calculate_campaign_roi(channel, budget)
            
            assert result.channel == channel
            assert result.budget == budget
            assert result.expected_customers >= 0
            assert result.expected_revenue >= 0
    
    def test_calculate_campaign_roi_with_custom_values(self):
        """Test ROI calculation with custom conversion rate and customer value"""
        result = roi_calc.calculate_campaign_roi(
            "linkedin_ads", 
            5000,
            custom_conversion_rate=0.05,
            custom_customer_value=3000
        )
        
        assert result.expected_customers > 0
        assert result.revenue_per_customer == 3000
    
    def test_calculate_campaign_roi_invalid_channel(self):
        """Test that invalid channel raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            roi_calc.calculate_campaign_roi("invalid_channel", 5000)
        
        assert "Unknown channel" in str(exc_info.value)
    
    def test_roi_result_to_dict(self):
        """Test converting ROI result to dictionary"""
        result = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict['channel'] == "linkedin_ads"
        assert result_dict['budget'] == 5000
        assert 'expected_customers' in result_dict
        assert 'expected_revenue' in result_dict
        assert 'roi_percentage' in result_dict
    
    def test_optimize_budget_allocation_three_channels(self):
        """Test optimizing budget across three channels"""
        allocation = roi_calc.optimize_budget_allocation(
            10000,
            ["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        # Verify allocation structure
        assert isinstance(allocation, BudgetAllocation)
        assert allocation.total_budget == 10000
        
        # Verify all three channels are allocated
        assert len(allocation.allocations) == 3
        assert "linkedin_ads" in allocation.allocations
        assert "content_marketing" in allocation.allocations
        assert "email_marketing" in allocation.allocations
        
        # Verify total allocation equals budget
        total_allocated = sum(allocation.allocations.values())
        assert abs(total_allocated - 10000) < 1  # Allow for small rounding errors
        
        # Verify percentages sum to 100%
        total_percentage = sum(allocation.allocation_percentages.values())
        assert abs(total_percentage - 100) < 0.1
        
        # Verify projected results exist for each channel
        assert len(allocation.projected_results) == 3
        
        # Verify overall metrics
        assert allocation.total_expected_customers > 0
        assert allocation.total_expected_revenue > 0
        assert allocation.overall_roi_percentage > 0
        
        # For 3 channels, expect 60/30/10 split (roughly)
        percentages = allocation.allocation_percentages
        sorted_pcts = sorted(percentages.values(), reverse=True)
        assert sorted_pcts[0] > 50  # Largest allocation > 50%
        assert sorted_pcts[1] > 20  # Second allocation > 20%
        assert sorted_pcts[2] < 20  # Smallest allocation < 20%
    
    def test_optimize_budget_allocation_single_channel(self):
        """Test optimizing budget for single channel"""
        allocation = roi_calc.optimize_budget_allocation(
            5000,
            ["linkedin_ads"]
        )
        
        assert len(allocation.allocations) == 1
        assert allocation.allocations["linkedin_ads"] == 5000
        assert allocation.allocation_percentages["linkedin_ads"] == 100.0
    
    def test_optimize_budget_allocation_two_channels(self):
        """Test optimizing budget for two channels"""
        allocation = roi_calc.optimize_budget_allocation(
            8000,
            ["linkedin_ads", "content_marketing"]
        )
        
        assert len(allocation.allocations) == 2
        
        # Should be roughly 70/30 split
        percentages = allocation.allocation_percentages
        sorted_pcts = sorted(percentages.values(), reverse=True)
        assert sorted_pcts[0] > 60  # Larger allocation
        assert sorted_pcts[1] < 40  # Smaller allocation
    
    def test_optimize_budget_allocation_with_constraints(self):
        """Test optimizing budget with min/max constraints"""
        constraints = {
            "linkedin_ads": (40, 60),  # min 40%, max 60%
            "content_marketing": (20, 40),  # min 20%, max 40%
            "email_marketing": (10, 30)  # min 10%, max 30%
        }
        
        allocation = roi_calc.optimize_budget_allocation(
            10000,
            ["linkedin_ads", "content_marketing", "email_marketing"],
            constraints=constraints
        )
        
        # Verify constraints are respected
        for channel, (min_pct, max_pct) in constraints.items():
            actual_pct = allocation.allocation_percentages[channel]
            assert min_pct <= actual_pct <= max_pct + 0.1  # Small tolerance for rounding
    
    def test_optimize_budget_allocation_invalid_channel(self):
        """Test that invalid channel raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            roi_calc.optimize_budget_allocation(
                10000,
                ["linkedin_ads", "invalid_channel"]
            )
        
        assert "Unknown channel" in str(exc_info.value)
    
    def test_budget_allocation_to_dict(self):
        """Test converting budget allocation to dictionary"""
        allocation = roi_calc.optimize_budget_allocation(
            10000,
            ["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        allocation_dict = allocation.to_dict()
        
        assert isinstance(allocation_dict, dict)
        assert allocation_dict['total_budget'] == 10000
        assert 'allocations' in allocation_dict
        assert 'allocation_percentages' in allocation_dict
        assert 'projected_results' in allocation_dict
        assert 'total_expected_customers' in allocation_dict
        assert 'total_expected_revenue' in allocation_dict
        assert 'overall_roi_percentage' in allocation_dict
    
    def test_roi_scales_with_budget(self):
        """Test that customers and revenue scale with budget"""
        result_1000 = roi_calc.calculate_campaign_roi("linkedin_ads", 1000)
        result_5000 = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)
        
        # More budget should result in more customers and revenue
        assert result_5000.expected_customers > result_1000.expected_customers
        assert result_5000.expected_revenue > result_1000.expected_revenue
    
    def test_different_channels_have_different_performance(self):
        """Test that different channels have different performance characteristics"""
        budget = 5000
        
        linkedin_result = roi_calc.calculate_campaign_roi("linkedin_ads", budget)
        email_result = roi_calc.calculate_campaign_roi("email_marketing", budget)
        webinar_result = roi_calc.calculate_campaign_roi("webinars", budget)
        
        # Different channels should have different results
        # (Not testing specific values, just that they differ)
        results = [
            linkedin_result.expected_customers,
            email_result.expected_customers,
            webinar_result.expected_customers
        ]
        
        # At least two should be different
        assert len(set(results)) > 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
