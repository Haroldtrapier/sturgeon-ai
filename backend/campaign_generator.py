"""
backend/campaign_generator.py
LinkedIn outreach campaign generation for Sturgeon AI
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    """Individual message in a campaign sequence"""
    sequence_number: int
    subject: Optional[str] = None
    content: str
    wait_days: int
    message_type: str  # 'connection', 'follow_up', 'value_prop', etc.


class TargetingCriteria(BaseModel):
    """LinkedIn targeting criteria"""
    job_titles: List[str]
    industries: List[str]
    company_size: List[str]
    seniority_levels: List[str]
    locations: Optional[List[str]] = None


class CampaignMetrics(BaseModel):
    """Expected campaign performance metrics"""
    expected_connection_rate: float
    expected_response_rate: float
    expected_meeting_rate: float
    expected_conversion_rate: float
    estimated_reach: int


class LinkedInCampaign(BaseModel):
    """Complete LinkedIn outreach campaign"""
    campaign_id: str
    target_persona: str
    target_count: int
    messages: List[Message]
    targeting: TargetingCriteria
    metrics: CampaignMetrics
    created_at: str


class CampaignGenerator:
    """Generator for LinkedIn outreach campaigns"""
    
    def __init__(self):
        self.persona_templates = {
            "bd_director": {
                "job_titles": ["Business Development Director", "Director of Business Development", 
                              "VP Business Development", "Head of Business Development"],
                "industries": ["Technology", "Software", "SaaS", "Professional Services"],
                "company_size": ["51-200", "201-500", "501-1000", "1001-5000"],
                "seniority_levels": ["Director", "VP", "C-Level"],
            },
            "sales_manager": {
                "job_titles": ["Sales Manager", "Sales Director", "Head of Sales", "VP Sales"],
                "industries": ["Technology", "Software", "B2B Services"],
                "company_size": ["11-50", "51-200", "201-500"],
                "seniority_levels": ["Manager", "Director", "VP"],
            },
            "marketing_director": {
                "job_titles": ["Marketing Director", "CMO", "VP Marketing", "Head of Marketing"],
                "industries": ["Technology", "E-commerce", "Consumer Goods"],
                "company_size": ["51-200", "201-500", "501-1000"],
                "seniority_levels": ["Director", "VP", "C-Level"],
            }
        }
        
        self.message_templates = {
            "bd_director": [
                {
                    "sequence_number": 1,
                    "subject": None,
                    "content": "Hi {first_name}, I noticed your work in business development at {company}. "
                              "Our platform helps companies like yours streamline government contracting workflows. "
                              "Would love to connect and share some insights that have helped similar teams increase win rates by 35%.",
                    "wait_days": 0,
                    "message_type": "connection"
                },
                {
                    "sequence_number": 2,
                    "subject": None,
                    "content": "Thanks for connecting! I wanted to share a quick case study of how {similar_company} "
                              "used our AI-powered contract matching to identify $2.3M in qualified opportunities they would have missed. "
                              "Would a 15-minute call work to explore if there's a fit for {company}?",
                    "wait_days": 3,
                    "message_type": "follow_up"
                },
                {
                    "sequence_number": 3,
                    "subject": None,
                    "content": "Hi {first_name}, following up on my last message. I know BD teams are often stretched thin. "
                              "Our clients typically see 40% time savings on proposal prep and a 25% increase in qualified pipeline. "
                              "Are these metrics interesting for your team's goals this quarter?",
                    "wait_days": 4,
                    "message_type": "value_prop"
                },
                {
                    "sequence_number": 4,
                    "subject": None,
                    "content": "Quick question - are you currently using any AI tools for contract intelligence or proposal generation? "
                              "I'd love to understand your current process and share how companies in {industry} are automating 60% of their workflow. "
                              "Open to a brief conversation?",
                    "wait_days": 5,
                    "message_type": "engagement"
                },
                {
                    "sequence_number": 5,
                    "subject": None,
                    "content": "Hi {first_name}, I don't want to be a pest, but I genuinely believe there's value here for {company}. "
                              "If timing isn't right now, totally understand. Would it make sense to reconnect next quarter? "
                              "Either way, happy to share our free industry benchmark report on government contracting trends.",
                    "wait_days": 7,
                    "message_type": "final_touchpoint"
                }
            ]
        }
    
    def generate_linkedin_outreach_campaign(
        self, 
        target_persona: str = "bd_director", 
        target_count: int = 100
    ) -> Dict:
        """
        Generate a complete LinkedIn outreach campaign
        
        Args:
            target_persona: Type of persona to target (bd_director, sales_manager, etc.)
            target_count: Number of prospects to target
            
        Returns:
            Dictionary with complete 5-message sequence, targeting, and metrics
        """
        if target_persona not in self.persona_templates:
            target_persona = "bd_director"
        
        # Get persona-specific targeting
        targeting_data = self.persona_templates[target_persona]
        targeting = TargetingCriteria(
            job_titles=targeting_data["job_titles"],
            industries=targeting_data["industries"],
            company_size=targeting_data["company_size"],
            seniority_levels=targeting_data["seniority_levels"],
            locations=["United States", "Canada", "United Kingdom"]
        )
        
        # Get message sequence
        message_templates = self.message_templates.get(
            target_persona, 
            self.message_templates["bd_director"]
        )
        messages = [Message(**msg) for msg in message_templates]
        
        # Calculate expected metrics based on industry benchmarks
        metrics = CampaignMetrics(
            expected_connection_rate=0.25,  # 25% connection acceptance
            expected_response_rate=0.15,     # 15% response rate
            expected_meeting_rate=0.08,      # 8% book a meeting
            expected_conversion_rate=0.03,   # 3% convert to opportunity
            estimated_reach=target_count
        )
        
        # Create campaign
        campaign = LinkedInCampaign(
            campaign_id=f"LI-{target_persona.upper()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            target_persona=target_persona,
            target_count=target_count,
            messages=messages,
            targeting=targeting,
            metrics=metrics,
            created_at=datetime.now().isoformat()
        )
        
        return campaign.model_dump()


# Create singleton instance for easy import
campaign_gen = CampaignGenerator()
