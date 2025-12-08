"""
Tests for campaign_gen module
"""

import pytest
from campaign_generator import campaign_gen


class TestGenerateLinkedInOutreachCampaign:
    """Test suite for generate_linkedin_outreach_campaign function"""
    
    def test_basic_bd_director_campaign(self):
        """Test basic campaign generation for BD director persona"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        # Verify structure
        assert "messages" in campaign
        assert "targeting" in campaign
        assert "metrics" in campaign
        assert "campaign_summary" in campaign
    
    def test_five_message_sequence(self):
        """Test that campaign generates exactly 5 messages"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        assert len(campaign["messages"]) == 5
        
        # Verify each message has required fields
        for i, msg in enumerate(campaign["messages"], 1):
            assert msg["sequence_number"] == i
            assert "subject" in msg
            assert "body" in msg
            assert "delay_days" in msg
            assert "personalization_fields" in msg
    
    def test_message_spacing(self):
        """Test that messages are properly spaced over time"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        # Messages should be spaced 3 days apart
        expected_delays = [0, 3, 6, 9, 12]
        actual_delays = [msg["delay_days"] for msg in campaign["messages"]]
        
        assert actual_delays == expected_delays
    
    def test_targeting_criteria(self):
        """Test that targeting includes all necessary criteria"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        targeting = campaign["targeting"]
        
        # Verify all targeting fields are present
        assert "persona" in targeting
        assert "persona_title" in targeting
        assert "job_titles" in targeting
        assert "industries" in targeting
        assert "seniority_levels" in targeting
        assert "company_sizes" in targeting
        assert "locations" in targeting
        assert "interests" in targeting
        assert "estimated_audience_size" in targeting
        assert "target_count" in targeting
        
        # Verify data types
        assert isinstance(targeting["job_titles"], list)
        assert isinstance(targeting["industries"], list)
        assert len(targeting["job_titles"]) > 0
        assert targeting["target_count"] == 100
    
    def test_metrics_calculation(self):
        """Test that metrics are calculated correctly"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        metrics = campaign["metrics"]
        
        # Verify metric fields
        assert "target_count" in metrics
        assert "expected_connection_accepts" in metrics
        assert "expected_message_opens" in metrics
        assert "expected_responses" in metrics
        assert "expected_demo_bookings" in metrics
        assert "estimated_conversion_rates" in metrics
        assert "estimated_roi" in metrics
        
        # Verify calculations are reasonable
        assert metrics["expected_connection_accepts"] <= metrics["target_count"]
        assert metrics["expected_responses"] <= metrics["expected_connection_accepts"]
    
    def test_campaign_summary(self):
        """Test campaign summary contains required information"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        summary = campaign["campaign_summary"]
        
        assert summary["campaign_type"] == "LinkedIn Outreach"
        assert summary["target_persona"] == "bd_director"
        assert summary["message_sequence_length"] == 5
        assert summary["total_campaign_duration_days"] == 12
        assert summary["status"] == "ready"
        assert "created_at" in summary
        assert "estimated_completion_date" in summary
    
    def test_procurement_officer_persona(self):
        """Test campaign generation for procurement officer persona"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="procurement_officer",
            target_count=50
        )
        
        assert campaign["targeting"]["persona"] == "procurement_officer"
        assert campaign["targeting"]["target_count"] == 50
        assert len(campaign["messages"]) == 5
    
    def test_grant_manager_persona(self):
        """Test campaign generation for grant manager persona"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="grant_manager",
            target_count=75
        )
        
        assert campaign["targeting"]["persona"] == "grant_manager"
        assert campaign["targeting"]["target_count"] == 75
        assert len(campaign["messages"]) == 5
    
    def test_invalid_persona_raises_error(self):
        """Test that invalid persona raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            campaign_gen.generate_linkedin_outreach_campaign(
                target_persona="invalid_persona",
                target_count=100
            )
        
        assert "Unknown target_persona" in str(exc_info.value)
        assert "invalid_persona" in str(exc_info.value)
    
    def test_negative_target_count_raises_error(self):
        """Test that negative target count raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            campaign_gen.generate_linkedin_outreach_campaign(
                target_persona="bd_director",
                target_count=-10
            )
        
        assert "target_count must be positive" in str(exc_info.value)
    
    def test_zero_target_count_raises_error(self):
        """Test that zero target count raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            campaign_gen.generate_linkedin_outreach_campaign(
                target_persona="bd_director",
                target_count=0
            )
        
        assert "target_count must be positive" in str(exc_info.value)
    
    def test_custom_sender_name(self):
        """Test that custom sender name is accepted"""
        custom_sender = "John Doe"
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100,
            sender_name=custom_sender
        )
        
        # Sender name is stored in campaign summary
        assert campaign["campaign_summary"]["sender"] == custom_sender
    
    def test_different_target_counts(self):
        """Test campaigns with different target counts"""
        for count in [10, 50, 100, 500, 1000]:
            campaign = campaign_gen.generate_linkedin_outreach_campaign(
                target_persona="bd_director",
                target_count=count
            )
            
            assert campaign["metrics"]["target_count"] == count
            assert campaign["targeting"]["target_count"] == count
            
            # Verify metrics scale with target count
            expected_connections = int(count * 0.25)
            assert campaign["metrics"]["expected_connection_accepts"] == expected_connections
    
    def test_personalization_fields(self):
        """Test that personalization fields are included in messages"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        for msg in campaign["messages"]:
            assert "personalization_fields" in msg
            assert isinstance(msg["personalization_fields"], list)
            # Common personalization fields should be present
            fields_str = " ".join(msg["personalization_fields"])
            assert "first_name" in fields_str or "{first_name}" in msg["body"]
