"""
backend/roi_calculator.py
ROI calculation and budget optimization for marketing campaigns
"""

from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel


class CampaignROI(BaseModel):
    """ROI calculation results for a campaign"""
    campaign_type: str
    budget: float
    expected_customers: int
    expected_revenue: float
    roi_percentage: float
    cost_per_customer: float
    customer_lifetime_value: float


class BudgetAllocation(BaseModel):
    """Optimal budget allocation across channels"""
    total_budget: float
    allocations: Dict[str, Dict[str, float]]  # channel -> {budget, percentage, expected_roi}
    total_expected_revenue: float
    total_expected_customers: int
    blended_roi: float


class ROICalculator:
    """Calculator for marketing campaign ROI and budget optimization"""
    
    def __init__(self):
        # Industry benchmarks for different marketing channels
        self.channel_metrics = {
            "linkedin_ads": {
                "cost_per_lead": 65,
                "lead_to_customer_rate": 0.24,  # 24% conversion
                "avg_customer_value": 2388,  # Average contract value
                "ltv_multiplier": 1.0,  # Lifetime value multiplier
            },
            "content_marketing": {
                "cost_per_lead": 55,
                "lead_to_customer_rate": 0.10,  # 10% conversion
                "avg_customer_value": 2200,
                "ltv_multiplier": 3.0,
            },
            "email_marketing": {
                "cost_per_lead": 45,
                "lead_to_customer_rate": 0.06,  # 6% conversion
                "avg_customer_value": 1850,
                "ltv_multiplier": 2.5,
            },
            "google_ads": {
                "cost_per_lead": 85,
                "lead_to_customer_rate": 0.10,  # 10% conversion
                "avg_customer_value": 2200,
                "ltv_multiplier": 3.0,
            },
            "linkedin_outreach": {
                "cost_per_lead": 65,
                "lead_to_customer_rate": 0.15,  # 15% conversion
                "avg_customer_value": 2500,
                "ltv_multiplier": 3.5,
            },
            "webinars": {
                "cost_per_lead": 110,
                "lead_to_customer_rate": 0.14,  # 14% conversion
                "avg_customer_value": 2600,
                "ltv_multiplier": 3.3,
            }
        }
    
    def calculate_campaign_roi(
        self, 
        campaign_type: str, 
        budget: float
    ) -> Dict:
        """
        Calculate expected ROI for a marketing campaign
        
        Args:
            campaign_type: Type of marketing campaign (linkedin_ads, content_marketing, etc.)
            budget: Campaign budget in dollars
            
        Returns:
            Dictionary with expected customers, revenue, and ROI percentage
        """
        if campaign_type not in self.channel_metrics:
            # Default to linkedin_ads metrics if unknown channel
            campaign_type = "linkedin_ads"
        
        metrics = self.channel_metrics[campaign_type]
        
        # Calculate number of leads from budget
        num_leads = budget / metrics["cost_per_lead"]
        
        # Calculate expected customers
        expected_customers = int(num_leads * metrics["lead_to_customer_rate"])
        
        # Calculate expected revenue (using lifetime value)
        customer_lifetime_value = metrics["avg_customer_value"] * metrics["ltv_multiplier"]
        expected_revenue = expected_customers * customer_lifetime_value
        
        # Calculate ROI percentage
        roi_percentage = ((expected_revenue - budget) / budget) * 100 if budget > 0 else 0
        
        # Calculate cost per customer
        cost_per_customer = budget / expected_customers if expected_customers > 0 else 0
        
        result = CampaignROI(
            campaign_type=campaign_type,
            budget=budget,
            expected_customers=expected_customers,
            expected_revenue=round(expected_revenue, 2),
            roi_percentage=round(roi_percentage, 1),
            cost_per_customer=round(cost_per_customer, 2),
            customer_lifetime_value=round(customer_lifetime_value, 2)
        )
        
        return result.model_dump()
    
    def optimize_budget_allocation(
        self, 
        total_budget: float, 
        channels: List[str]
    ) -> Dict:
        """
        Optimize budget allocation across multiple marketing channels
        
        Args:
            total_budget: Total marketing budget to allocate
            channels: List of marketing channels to consider
            
        Returns:
            Dictionary with optimal allocation percentages and projections
        """
        # Validate channels
        valid_channels = [ch for ch in channels if ch in self.channel_metrics]
        if not valid_channels:
            valid_channels = ["linkedin_ads", "content_marketing", "email_marketing"]
        
        # Calculate efficiency score for each channel (ROI per dollar)
        channel_scores = {}
        for channel in valid_channels:
            # Calculate ROI for a standard $1000 budget
            test_roi = self.calculate_campaign_roi(channel, 1000)
            efficiency = test_roi["roi_percentage"] / 100  # Convert to decimal
            channel_scores[channel] = efficiency
        
        # Sort channels by efficiency
        sorted_channels = sorted(
            channel_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Allocate budget based on efficiency with diminishing returns
        # Top channel gets more, but we diversify to reduce risk
        allocations = {}
        
        if len(sorted_channels) == 1:
            # All budget to single channel
            allocations[sorted_channels[0][0]] = 1.0
        elif len(sorted_channels) == 2:
            # 70/30 split
            allocations[sorted_channels[0][0]] = 0.70
            allocations[sorted_channels[1][0]] = 0.30
        elif len(sorted_channels) >= 3:
            # 60/30/10 split for top 3, or spread remaining
            allocations[sorted_channels[0][0]] = 0.60
            allocations[sorted_channels[1][0]] = 0.30
            
            remaining = 0.10
            remaining_channels = sorted_channels[2:]
            if remaining_channels:
                per_channel = remaining / len(remaining_channels)
                for channel, _ in remaining_channels:
                    allocations[channel] = per_channel
        
        # Calculate projections for each allocation
        allocation_details = {}
        total_customers = 0
        total_revenue = 0.0
        
        for channel, percentage in allocations.items():
            channel_budget = total_budget * percentage
            roi_result = self.calculate_campaign_roi(channel, channel_budget)
            
            allocation_details[channel] = {
                "budget": round(channel_budget, 2),
                "percentage": round(percentage * 100, 1),
                "expected_customers": roi_result["expected_customers"],
                "expected_revenue": roi_result["expected_revenue"],
                "expected_roi": roi_result["roi_percentage"]
            }
            
            total_customers += roi_result["expected_customers"]
            total_revenue += roi_result["expected_revenue"]
        
        # Calculate blended ROI
        blended_roi = ((total_revenue - total_budget) / total_budget) * 100 if total_budget > 0 else 0
        
        result = BudgetAllocation(
            total_budget=total_budget,
            allocations=allocation_details,
            total_expected_revenue=round(total_revenue, 2),
            total_expected_customers=total_customers,
            blended_roi=round(blended_roi, 1)
        )
        
        return result.model_dump()


# Create singleton instance for easy import
roi_calc = ROICalculator()
