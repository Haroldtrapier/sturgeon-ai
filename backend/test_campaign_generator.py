"""
Tests for campaign_generator module
"""

import pytest
from campaign_generator import campaign_gen, CampaignGenerator, LinkedInCampaign


class TestCampaignGenerator:
    """Test cases for CampaignGenerator class"""
    
    def test_generate_linkedin_campaign_bd_director(self):
        """Test generating campaign for BD Director persona"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        # Verify campaign structure
        assert isinstance(campaign, LinkedInCampaign)
        assert campaign.target_persona == "bd_director"
        assert campaign.target_count == 100
        assert campaign.campaign_id.startswith("LI-")
        
        # Verify messages
        assert len(campaign.messages) == 5
        assert campaign.messages[0].sequence_number == 1
        assert campaign.messages[4].sequence_number == 5
        
        # Verify all messages have required fields
        for msg in campaign.messages:
            assert msg.body is not None
            assert msg.call_to_action is not None
            assert msg.delay_days >= 0
        
        # Verify targeting criteria
        assert len(campaign.targeting.job_titles) > 0
        assert len(campaign.targeting.industries) > 0
        assert len(campaign.targeting.company_sizes) > 0
        
        # Verify metrics
        assert campaign.metrics.expected_open_rate > 0
        assert campaign.metrics.expected_response_rate > 0
        assert campaign.metrics.expected_conversion_rate > 0
        assert campaign.metrics.estimated_reach > 0
        assert campaign.metrics.estimated_responses > 0
    
    def test_generate_linkedin_campaign_different_personas(self):
        """Test generating campaigns for different personas"""
        personas = ["bd_director", "sales_manager", "cto", "marketing_director"]
        
        for persona in personas:
            campaign = campaign_gen.generate_linkedin_outreach_campaign(
                target_persona=persona,
                target_count=50
            )
            
            assert campaign.target_persona == persona
            assert len(campaign.messages) == 5
            assert campaign.metrics.estimated_conversions > 0
    
    def test_generate_linkedin_campaign_with_custom_name(self):
        """Test generating campaign with custom name"""
        custom_name = "Q4 2024 BD Outreach"
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100,
            campaign_name=custom_name
        )
        
        assert campaign.campaign_name == custom_name
    
    def test_generate_linkedin_campaign_with_locations(self):
        """Test generating campaign with custom locations"""
        locations = ["United States", "Germany", "France"]
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100,
            locations=locations
        )
        
        assert campaign.targeting.locations == locations
    
    def test_campaign_metrics_scale_with_target_count(self):
        """Test that metrics scale appropriately with target count"""
        campaign_small = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=50
        )
        
        campaign_large = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=200
        )
        
        # Larger target count should result in more estimated responses
        assert campaign_large.metrics.estimated_responses > campaign_small.metrics.estimated_responses
        assert campaign_large.metrics.estimated_conversions > campaign_small.metrics.estimated_conversions
    
    def test_campaign_to_dict(self):
        """Test converting campaign to dictionary"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        campaign_dict = campaign.to_dict()
        
        assert isinstance(campaign_dict, dict)
        assert campaign_dict['target_persona'] == "bd_director"
        assert campaign_dict['target_count'] == 100
        assert 'messages' in campaign_dict
        assert 'targeting' in campaign_dict
        assert 'metrics' in campaign_dict
        assert len(campaign_dict['messages']) == 5
    
    def test_invalid_persona_defaults_to_bd_director(self):
        """Test that invalid persona defaults to bd_director"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="invalid_persona",
            target_count=100
        )
        
        # Should default to bd_director
        assert campaign.target_persona == "bd_director"
        assert len(campaign.messages) == 5
    
    def test_message_sequence_has_correct_delays(self):
        """Test that message sequence has appropriate delays"""
        campaign = campaign_gen.generate_linkedin_outreach_campaign(
            target_persona="bd_director",
            target_count=100
        )
        
        # First message should have 0 delay
        assert campaign.messages[0].delay_days == 0
        
        # Subsequent messages should have increasing delays
        for i in range(1, len(campaign.messages)):
            assert campaign.messages[i].delay_days > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
