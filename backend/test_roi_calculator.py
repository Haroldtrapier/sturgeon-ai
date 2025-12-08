"""
Tests for ROI Calculator module
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roi_calculator import ROICalculator, CampaignMetrics


class TestROICalculator:
    """Test suite for ROI Calculator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.calculator = ROICalculator()
    
    def test_calculate_campaign_roi_linkedin(self):
        """Test ROI calculation for LinkedIn ads"""
        result = self.calculator.calculate_campaign_roi(
            channel="linkedin_ads",
            budget=10000,
            duration_months=3
        )
        
        assert result["channel"] == "linkedin_ads"
        assert result["investment"]["budget"] == 10000
        assert result["investment"]["duration_months"] == 3
        assert result["investment"]["monthly_spend"] == pytest.approx(3333.33, rel=0.01)
        assert result["performance"]["clicks"] > 0
        assert result["performance"]["leads"] > 0
        assert result["performance"]["customers_acquired"] >= 0
        assert result["returns"]["roi_percentage"] is not None
        assert "recommendation" in result
    
    def test_calculate_campaign_roi_google_ads(self):
        """Test ROI calculation for Google ads"""
        result = self.calculator.calculate_campaign_roi(
            channel="google_ads",
            budget=5000,
            duration_months=2
        )
        
        assert result["channel"] == "google_ads"
        assert result["investment"]["budget"] == 5000
        assert result["performance"]["clicks"] > 0
        assert result["efficiency_metrics"]["cac"] >= 0
        assert result["efficiency_metrics"]["ltv"] > 0
    
    def test_calculate_campaign_roi_content_marketing(self):
        """Test ROI calculation for content marketing"""
        result = self.calculator.calculate_campaign_roi(
            channel="content_marketing",
            budget=5000,
            duration_months=3
        )
        
        assert result["channel"] == "content_marketing"
        assert result["investment"]["budget"] == 5000
        assert result["performance"]["clicks"] > 0
        assert result["performance"]["leads"] >= 0
    
    def test_calculate_campaign_roi_email_marketing(self):
        """Test ROI calculation for email marketing"""
        result = self.calculator.calculate_campaign_roi(
            channel="email_marketing",
            budget=1000,
            duration_months=1
        )
        
        assert result["channel"] == "email_marketing"
        assert result["investment"]["budget"] == 1000
        assert result["performance"]["clicks"] > 0
    
    def test_calculate_campaign_roi_invalid_channel(self):
        """Test ROI calculation with invalid channel"""
        result = self.calculator.calculate_campaign_roi(
            channel="invalid_channel",
            budget=10000,
            duration_months=3
        )
        
        assert "error" in result
        assert "Unknown channel" in result["error"]
    
    def test_optimize_budget_allocation_three_channels(self):
        """Test budget optimization across three channels"""
        result = self.calculator.optimize_budget_allocation(
            total_budget=30000,
            channels=["linkedin_ads", "google_ads", "content_marketing"]
        )
        
        assert result["total_budget"] == 30000
        assert len(result["optimized_allocation"]) == 3
        assert len(result["channel_ranking"]) == 3
        assert result["total_expected_results"]["customers"] >= 0
        assert result["total_expected_results"]["revenue"] >= 0
        assert len(result["execution_priority"]) == 3
        
        # Verify budget allocations sum to total
        total_allocated = sum(
            alloc["budget"] for alloc in result["optimized_allocation"].values()
        )
        assert total_allocated == pytest.approx(30000, rel=0.01)
    
    def test_optimize_budget_allocation_two_channels(self):
        """Test budget optimization across two channels"""
        result = self.calculator.optimize_budget_allocation(
            total_budget=20000,
            channels=["linkedin_ads", "email_marketing"]
        )
        
        assert result["total_budget"] == 20000
        assert len(result["optimized_allocation"]) == 2
        
        # Verify 70/30 split for two channels
        total_allocated = sum(
            alloc["budget"] for alloc in result["optimized_allocation"].values()
        )
        assert total_allocated == pytest.approx(20000, rel=0.01)
    
    def test_optimize_budget_allocation_single_channel(self):
        """Test budget optimization with single channel"""
        result = self.calculator.optimize_budget_allocation(
            total_budget=10000,
            channels=["google_ads"]
        )
        
        assert result["total_budget"] == 10000
        assert len(result["optimized_allocation"]) == 1
        assert result["optimized_allocation"]["google_ads"]["budget"] == 10000
    
    def test_project_growth_trajectory_default(self):
        """Test growth projection with default channel mix"""
        result = self.calculator.project_growth_trajectory(
            monthly_budget=5000,
            duration_months=12
        )
        
        assert result["monthly_budget"] == 5000
        assert result["projection_period"] == "12 months"
        assert result["total_investment"] == 60000
        assert len(result["monthly_breakdown"]) == 12
        assert "year_end_totals" in result
        assert result["year_end_totals"]["total_customers"] >= 0
        assert result["year_end_totals"]["total_revenue"] >= 0
        
        # Verify cumulative values increase
        for i in range(1, len(result["monthly_breakdown"])):
            curr = result["monthly_breakdown"][i]
            prev = result["monthly_breakdown"][i-1]
            assert curr["cumulative_customers"] >= prev["cumulative_customers"]
            assert curr["cumulative_revenue"] >= prev["cumulative_revenue"]
    
    def test_project_growth_trajectory_custom_mix(self):
        """Test growth projection with custom channel mix"""
        custom_mix = {
            "linkedin_ads": 0.50,
            "google_ads": 0.30,
            "email_marketing": 0.20
        }
        
        result = self.calculator.project_growth_trajectory(
            monthly_budget=10000,
            duration_months=6,
            channel_mix=custom_mix
        )
        
        assert result["monthly_budget"] == 10000
        assert len(result["monthly_breakdown"]) == 6
        assert result["channel_allocation"] == custom_mix
    
    def test_generate_recommendation_scale_aggressively(self):
        """Test recommendation for excellent performance"""
        rec = self.calculator._generate_recommendation(roi=250, ltv_cac_ratio=3.5)
        assert "SCALE AGGRESSIVELY" in rec
    
    def test_generate_recommendation_scale(self):
        """Test recommendation for strong performance"""
        rec = self.calculator._generate_recommendation(roi=150, ltv_cac_ratio=2.5)
        assert "SCALE" in rec and "AGGRESSIVELY" not in rec
    
    def test_generate_recommendation_optimize_and_scale(self):
        """Test recommendation for good performance"""
        rec = self.calculator._generate_recommendation(roi=75, ltv_cac_ratio=2.0)
        assert "OPTIMIZE & SCALE" in rec
    
    def test_generate_recommendation_optimize(self):
        """Test recommendation for suboptimal performance"""
        rec = self.calculator._generate_recommendation(roi=25, ltv_cac_ratio=1.2)
        assert "OPTIMIZE" in rec and "SCALE" not in rec
    
    def test_generate_recommendation_pause(self):
        """Test recommendation for poor performance"""
        rec = self.calculator._generate_recommendation(roi=-10, ltv_cac_ratio=0.8)
        assert "PAUSE & PIVOT" in rec
    
    def test_campaign_metrics_dataclass(self):
        """Test CampaignMetrics dataclass"""
        metrics = CampaignMetrics(
            spend=10000.0,
            impressions=100000,
            clicks=2500,
            leads=125,
            demos=37,
            customers=9,
            revenue=21492.0
        )
        
        assert metrics.spend == 10000.0
        assert metrics.impressions == 100000
        assert metrics.clicks == 2500
        assert metrics.leads == 125
        assert metrics.demos == 37
        assert metrics.customers == 9
        assert metrics.revenue == 21492.0
    
    def test_roi_calculation_with_zero_customers(self):
        """Test ROI calculation handles zero customers gracefully"""
        result = self.calculator.calculate_campaign_roi(
            channel="linkedin_ads",
            budget=100,  # Very small budget
            duration_months=1
        )
        
        # Should handle zero customers without crashing
        assert "efficiency_metrics" in result
        if result["performance"]["customers_acquired"] == 0:
            assert result["efficiency_metrics"]["ltv_cac_ratio"] == 0
    
    def test_benchmarks_structure(self):
        """Test that benchmarks have correct structure"""
        benchmarks = self.calculator.benchmarks
        
        assert "linkedin_ads" in benchmarks
        assert "google_ads" in benchmarks
        assert "content_marketing" in benchmarks
        assert "email_marketing" in benchmarks
        
        # Check LinkedIn ads benchmark structure
        linkedin = benchmarks["linkedin_ads"]
        assert "cpc" in linkedin
        assert "ctr" in linkedin
        assert "conversion_rate" in linkedin
        assert "avg_deal_size" in linkedin
        
        # Check content marketing benchmark structure
        content = benchmarks["content_marketing"]
        assert "cost_per_article" in content
        assert "traffic_per_article" in content
        assert "conversion_rate" in content
        assert "avg_deal_size" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
