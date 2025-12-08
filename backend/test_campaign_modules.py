"""
backend/test_campaign_modules.py
Tests for campaign_generator and roi_calculator modules
"""

import pytest
from campaign_generator import campaign_gen, CampaignGenerator
from roi_calculator import roi_calc, ROICalculator


class TestCampaignGenerator:
    """Tests for LinkedIn campaign generation"""
    
    def test_generate_linkedin_campaign_basic(self):
        """Test basic campaign generation"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        # Verify structure
        assert "campaign_id" in campaign
        assert "target_persona" in campaign
        assert "target_count" in campaign
        assert "messages" in campaign
        assert "targeting" in campaign
        assert "metrics" in campaign
        
        # Verify values
        assert campaign["target_persona"] == "bd_director"
        assert campaign["target_count"] == 100
        assert len(campaign["messages"]) == 5
    
    def test_campaign_messages_sequence(self):
        """Test message sequence is complete and ordered"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign()
        messages = campaign["messages"]
        
        # Verify 5 messages
        assert len(messages) == 5
        
        # Verify sequence numbers
        for i, msg in enumerate(messages, 1):
            assert msg["sequence_number"] == i
            assert "content" in msg
            assert "wait_days" in msg
            assert "message_type" in msg
    
    def test_campaign_targeting(self):
        """Test targeting criteria"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign()
        targeting = campaign["targeting"]
        
        assert "job_titles" in targeting
        assert "industries" in targeting
        assert "company_size" in targeting
        assert "seniority_levels" in targeting
        assert len(targeting["job_titles"]) > 0
        assert len(targeting["industries"]) > 0
    
    def test_campaign_metrics(self):
        """Test campaign metrics"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign()
        metrics = campaign["metrics"]
        
        assert "expected_connection_rate" in metrics
        assert "expected_response_rate" in metrics
        assert "expected_meeting_rate" in metrics
        assert "expected_conversion_rate" in metrics
        assert "estimated_reach" in metrics
        
        # Verify rates are between 0 and 1
        assert 0 <= metrics["expected_connection_rate"] <= 1
        assert 0 <= metrics["expected_response_rate"] <= 1
        assert 0 <= metrics["expected_meeting_rate"] <= 1
        assert 0 <= metrics["expected_conversion_rate"] <= 1
    
    def test_different_personas(self):
        """Test generation for different personas"""
        personas = ["bd_director", "sales_manager", "marketing_director"]
        
        for persona in personas:
            campaign = campaign_gen.generate_linkedin_outreach_campaign(
                target_persona=persona,
                target_count=50
            )
            assert campaign["target_persona"] == persona
            assert campaign["target_count"] == 50


class TestROICalculator:
    """Tests for ROI calculation and budget optimization"""
    
    def test_calculate_campaign_roi_basic(self):
        """Test basic ROI calculation"""
        roi = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)
        
        # Verify structure
        assert "campaign_type" in roi
        assert "budget" in roi
        assert "expected_customers" in roi
        assert "expected_revenue" in roi
        assert "roi_percentage" in roi
        assert "cost_per_customer" in roi
        assert "customer_lifetime_value" in roi
        
        # Verify values
        assert roi["campaign_type"] == "linkedin_ads"
        assert roi["budget"] == 5000
        assert roi["expected_customers"] > 0
        assert roi["expected_revenue"] > 0
    
    def test_calculate_campaign_roi_exact_values(self):
        """Test ROI calculation matches expected values from problem statement"""
        roi = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)
        
        # These are the expected values from the problem statement
        assert roi["expected_customers"] == 18
        assert roi["expected_revenue"] == 42984.0
        assert roi["roi_percentage"] == 759.7
    
    def test_calculate_roi_different_channels(self):
        """Test ROI calculation for different channels"""
        channels = ["linkedin_ads", "content_marketing", "email_marketing"]
        
        for channel in channels:
            roi = roi_calc.calculate_campaign_roi(channel, 1000)
            assert roi["campaign_type"] == channel
            assert roi["budget"] == 1000
            assert roi["expected_customers"] >= 0
            assert roi["expected_revenue"] >= 0
    
    def test_optimize_budget_allocation_basic(self):
        """Test basic budget allocation"""
        allocation = roi_calc.optimize_budget_allocation(
            10000,
            ["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        # Verify structure
        assert "total_budget" in allocation
        assert "allocations" in allocation
        assert "total_expected_revenue" in allocation
        assert "total_expected_customers" in allocation
        assert "blended_roi" in allocation
        
        # Verify values
        assert allocation["total_budget"] == 10000
        assert len(allocation["allocations"]) == 3
    
    def test_budget_allocation_sums_to_total(self):
        """Test that budget allocations sum to total"""
        allocation = roi_calc.optimize_budget_allocation(
            10000,
            ["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        total_allocated = sum(
            alloc["budget"] 
            for alloc in allocation["allocations"].values()
        )
        
        # Allow for small floating point differences
        assert abs(total_allocated - 10000) < 0.01
    
    def test_budget_allocation_60_30_10_split(self):
        """Test that allocation creates 60/30/10 split for 3 channels"""
        allocation = roi_calc.optimize_budget_allocation(
            10000,
            ["linkedin_ads", "content_marketing", "email_marketing"]
        )
        
        percentages = sorted(
            [alloc["percentage"] for alloc in allocation["allocations"].values()],
            reverse=True
        )
        
        # Should be 60%, 30%, 10%
        assert percentages[0] == 60.0
        assert percentages[1] == 30.0
        assert percentages[2] == 10.0
    
    def test_budget_allocation_single_channel(self):
        """Test budget allocation with single channel"""
        allocation = roi_calc.optimize_budget_allocation(
            5000,
            ["linkedin_ads"]
        )
        
        assert len(allocation["allocations"]) == 1
        assert allocation["allocations"]["linkedin_ads"]["percentage"] == 100.0
    
    def test_roi_positive_for_valid_inputs(self):
        """Test that ROI is positive for valid inputs"""
        roi = roi_calc.calculate_campaign_roi("linkedin_ads", 1000)
        assert roi["roi_percentage"] > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
