"""
LinkedIn Campaign Generator Module

This module provides functionality to generate LinkedIn outreach campaigns
with multi-message sequences, targeting criteria, and performance metrics.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import random


@dataclass
class Message:
    """Represents a single message in the campaign sequence"""
    sequence_number: int
    subject: Optional[str]
    body: str
    delay_days: int
    call_to_action: str


@dataclass
class TargetingCriteria:
    """LinkedIn targeting criteria for the campaign"""
    job_titles: List[str]
    industries: List[str]
    company_sizes: List[str]
    locations: List[str]
    seniority_levels: List[str]


@dataclass
class CampaignMetrics:
    """Expected campaign performance metrics"""
    expected_open_rate: float
    expected_response_rate: float
    expected_conversion_rate: float
    estimated_reach: int
    estimated_responses: int
    estimated_conversions: int


@dataclass
class LinkedInCampaign:
    """Complete LinkedIn outreach campaign"""
    campaign_id: str
    campaign_name: str
    target_persona: str
    target_count: int
    messages: List[Message]
    targeting: TargetingCriteria
    metrics: CampaignMetrics
    created_at: str

    def to_dict(self) -> Dict:
        """Convert campaign to dictionary format"""
        return {
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'target_persona': self.target_persona,
            'target_count': self.target_count,
            'messages': [asdict(msg) for msg in self.messages],
            'targeting': asdict(self.targeting),
            'metrics': asdict(self.metrics),
            'created_at': self.created_at
        }


class CampaignGenerator:
    """Generator for LinkedIn outreach campaigns"""
    
    # Persona-specific templates and data
    PERSONA_DATA = {
        'bd_director': {
            'job_titles': ['Business Development Director', 'VP Business Development', 
                          'Director of Business Development', 'Head of Business Development'],
            'industries': ['Technology', 'SaaS', 'Enterprise Software', 'Professional Services'],
            'seniority_levels': ['Director', 'VP', 'C-Level'],
            'company_sizes': ['51-200', '201-500', '501-1000', '1001-5000'],
        },
        'sales_manager': {
            'job_titles': ['Sales Manager', 'Sales Director', 'Regional Sales Manager', 
                          'VP of Sales'],
            'industries': ['Technology', 'B2B Services', 'Manufacturing', 'Financial Services'],
            'seniority_levels': ['Manager', 'Director', 'VP'],
            'company_sizes': ['11-50', '51-200', '201-500', '501-1000'],
        },
        'cto': {
            'job_titles': ['CTO', 'Chief Technology Officer', 'VP Engineering', 
                          'Head of Engineering'],
            'industries': ['Technology', 'SaaS', 'Fintech', 'Enterprise Software'],
            'seniority_levels': ['VP', 'C-Level'],
            'company_sizes': ['51-200', '201-500', '501-1000', '1001-5000', '5000+'],
        },
        'marketing_director': {
            'job_titles': ['Marketing Director', 'VP Marketing', 'CMO', 
                          'Head of Marketing'],
            'industries': ['Technology', 'E-commerce', 'Consumer Goods', 'Professional Services'],
            'seniority_levels': ['Director', 'VP', 'C-Level'],
            'company_sizes': ['51-200', '201-500', '501-1000', '1001-5000'],
        }
    }
    
    MESSAGE_TEMPLATES = {
        'bd_director': [
            {
                'sequence_number': 1,
                'subject': 'Quick question about {company} BD strategy',
                'body': 'Hi {name},\n\nI noticed {company}\'s recent expansion in {industry}. As a BD Director, you\'re likely exploring new partnership opportunities.\n\nI work with companies similar to yours to accelerate their partnership pipeline by 40-60% through strategic introductions and deal flow optimization.\n\nWould you be open to a brief conversation about your current BD priorities?',
                'delay_days': 0,
                'call_to_action': 'Schedule a 15-minute call'
            },
            {
                'sequence_number': 2,
                'subject': None,
                'body': 'Hi {name},\n\nI wanted to follow up on my previous message. I understand you\'re busy managing multiple partnership initiatives.\n\nJust to give you context: we\'ve helped companies like {competitor1} and {competitor2} close deals 30% faster by streamlining their BD process.\n\nWould next Tuesday or Wednesday work for a quick call?',
                'delay_days': 3,
                'call_to_action': 'Reply with your availability'
            },
            {
                'sequence_number': 3,
                'subject': None,
                'body': 'Hi {name},\n\nI shared a case study in your inbox showing how we helped a {industry} company increase their partnership revenue by $2M in 6 months.\n\nGiven {company}\'s growth trajectory, I thought this might be relevant.\n\nWould you like me to send it over?',
                'delay_days': 4,
                'call_to_action': 'Request case study'
            },
            {
                'sequence_number': 4,
                'subject': None,
                'body': 'Hi {name},\n\nLast touch from me - I understand timing might not be right.\n\nIf you\'re interested in learning how companies in {industry} are leveraging strategic partnerships to grow 50% faster, I\'d be happy to share our framework.\n\nNo pressure either way.',
                'delay_days': 5,
                'call_to_action': 'Get the framework'
            },
            {
                'sequence_number': 5,
                'subject': None,
                'body': 'Hi {name},\n\nBreakup message here 😊 I\'ll stop reaching out.\n\nIf things change and you\'d like to discuss partnership strategies, feel free to reach out anytime.\n\nBest of luck with your BD initiatives at {company}!',
                'delay_days': 7,
                'call_to_action': 'Stay in touch'
            }
        ]
    }
    
    def generate_linkedin_outreach_campaign(
        self, 
        target_persona: str, 
        target_count: int,
        campaign_name: Optional[str] = None,
        locations: Optional[List[str]] = None
    ) -> LinkedInCampaign:
        """
        Generate a complete LinkedIn outreach campaign
        
        Args:
            target_persona: Type of persona to target (e.g., 'bd_director', 'cto')
            target_count: Number of prospects to target
            campaign_name: Optional custom campaign name
            locations: Optional list of target locations
            
        Returns:
            LinkedInCampaign: Complete campaign with messages, targeting, and metrics
        """
        # Validate persona
        if target_persona not in self.PERSONA_DATA:
            # Use bd_director as default if persona not found
            target_persona = 'bd_director'
        
        # Generate campaign ID
        campaign_id = f"LI-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        # Generate campaign name
        if not campaign_name:
            persona_label = target_persona.replace('_', ' ').title()
            campaign_name = f"{persona_label} Outreach - {datetime.now().strftime('%B %Y')}"
        
        # Get persona data
        persona_data = self.PERSONA_DATA[target_persona]
        
        # Create targeting criteria
        targeting = TargetingCriteria(
            job_titles=persona_data['job_titles'],
            industries=persona_data['industries'],
            company_sizes=persona_data['company_sizes'],
            locations=locations or ['United States', 'Canada', 'United Kingdom'],
            seniority_levels=persona_data['seniority_levels']
        )
        
        # Generate message sequence
        template_messages = self.MESSAGE_TEMPLATES.get(
            target_persona, 
            self.MESSAGE_TEMPLATES['bd_director']
        )
        
        messages = [
            Message(
                sequence_number=msg['sequence_number'],
                subject=msg['subject'],
                body=msg['body'],
                delay_days=msg['delay_days'],
                call_to_action=msg['call_to_action']
            )
            for msg in template_messages
        ]
        
        # Calculate expected metrics
        metrics = self._calculate_campaign_metrics(target_count, target_persona)
        
        # Create campaign
        campaign = LinkedInCampaign(
            campaign_id=campaign_id,
            campaign_name=campaign_name,
            target_persona=target_persona,
            target_count=target_count,
            messages=messages,
            targeting=targeting,
            metrics=metrics,
            created_at=datetime.now().isoformat()
        )
        
        return campaign
    
    def _calculate_campaign_metrics(
        self, 
        target_count: int, 
        persona: str
    ) -> CampaignMetrics:
        """
        Calculate expected campaign performance metrics
        
        Args:
            target_count: Number of prospects targeted
            persona: Target persona type
            
        Returns:
            CampaignMetrics: Expected performance metrics
        """
        # Persona-specific baseline rates (industry benchmarks)
        benchmark_rates = {
            'bd_director': {
                'open_rate': 0.65,
                'response_rate': 0.15,
                'conversion_rate': 0.08
            },
            'sales_manager': {
                'open_rate': 0.60,
                'response_rate': 0.12,
                'conversion_rate': 0.06
            },
            'cto': {
                'open_rate': 0.55,
                'response_rate': 0.10,
                'conversion_rate': 0.05
            },
            'marketing_director': {
                'open_rate': 0.62,
                'response_rate': 0.13,
                'conversion_rate': 0.07
            }
        }
        
        rates = benchmark_rates.get(persona, benchmark_rates['bd_director'])
        
        estimated_reach = int(target_count * rates['open_rate'])
        estimated_responses = int(target_count * rates['response_rate'])
        estimated_conversions = int(target_count * rates['conversion_rate'])
        
        return CampaignMetrics(
            expected_open_rate=rates['open_rate'],
            expected_response_rate=rates['response_rate'],
            expected_conversion_rate=rates['conversion_rate'],
            estimated_reach=estimated_reach,
            estimated_responses=estimated_responses,
            estimated_conversions=estimated_conversions
        )


# Create singleton instance
campaign_gen = CampaignGenerator()
