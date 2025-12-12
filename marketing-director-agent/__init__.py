"""
Marketing Director Agent Package

AI-powered marketing director agent with comprehensive capabilities for:
- Strategic marketing planning
- Campaign generation and management
- ROI analysis and budget optimization
- Audience targeting and segmentation
"""

from .agent_core import MarketingDirectorAgent
from .campaign_generator import CampaignGenerator, CampaignChannel, CampaignObjective
from .roi_calculator import ROICalculator

__version__ = "1.0.0"
__author__ = "Sturgeon AI"

__all__ = [
    'MarketingDirectorAgent',
    'CampaignGenerator',
    'CampaignChannel',
    'CampaignObjective',
    'ROICalculator',
]
