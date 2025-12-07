"""
ROI Calculator Module

This module provides functionality to calculate campaign ROI and optimize
budget allocation across different marketing channels.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import math


@dataclass
class ROIResult:
    """Results of ROI calculation"""
    channel: str
    budget: float
    expected_customers: int
    expected_revenue: float
    roi_percentage: float
    cost_per_customer: float
    revenue_per_customer: float

    def to_dict(self) -> Dict:
        """Convert ROI result to dictionary format"""
        return asdict(self)


@dataclass
class BudgetAllocation:
    """Optimized budget allocation across channels"""
    total_budget: float
    allocations: Dict[str, float]
    allocation_percentages: Dict[str, float]
    projected_results: Dict[str, ROIResult]
    total_expected_customers: int
    total_expected_revenue: float
    overall_roi_percentage: float

    def to_dict(self) -> Dict:
        """Convert budget allocation to dictionary format"""
        return {
            'total_budget': self.total_budget,
            'allocations': self.allocations,
            'allocation_percentages': self.allocation_percentages,
            'projected_results': {
                channel: result.to_dict() 
                for channel, result in self.projected_results.items()
            },
            'total_expected_customers': self.total_expected_customers,
            'total_expected_revenue': self.total_expected_revenue,
            'overall_roi_percentage': self.overall_roi_percentage
        }


class ROICalculator:
    """Calculator for marketing campaign ROI and budget optimization"""
    
    # Channel performance data based on industry benchmarks
    CHANNEL_DATA = {
        'linkedin_ads': {
            'cpc': 8.50,  # Cost per click
            'conversion_rate': 0.036,  # 3.6% of clicks convert
            'avg_customer_value': 2388,  # Average customer lifetime value
            'reach_efficiency': 0.85,  # 85% of budget goes to actual reach
        },
        'content_marketing': {
            'cost_per_lead': 92,  # Cost per qualified lead
            'conversion_rate': 0.08,  # 8% of leads convert
            'avg_customer_value': 3200,
            'reach_efficiency': 0.90,
        },
        'email_marketing': {
            'cost_per_send': 0.10,  # Cost per email sent
            'open_rate': 0.22,  # 22% open rate
            'click_rate': 0.03,  # 3% click through rate
            'conversion_rate': 0.015,  # 1.5% of clicks convert
            'avg_customer_value': 1850,
            'reach_efficiency': 0.95,
        },
        'google_ads': {
            'cpc': 5.20,
            'conversion_rate': 0.035,  # 3.5% conversion rate
            'avg_customer_value': 2100,
            'reach_efficiency': 0.80,
        },
        'social_media_ads': {
            'cpc': 3.80,
            'conversion_rate': 0.018,  # 1.8% conversion rate
            'avg_customer_value': 1650,
            'reach_efficiency': 0.82,
        },
        'seo': {
            'cost_per_lead': 65,
            'conversion_rate': 0.12,  # 12% conversion rate (high intent)
            'avg_customer_value': 2800,
            'reach_efficiency': 0.92,
        },
        'webinars': {
            'cost_per_attendee': 45,
            'conversion_rate': 0.15,  # 15% of attendees convert
            'avg_customer_value': 4200,
            'reach_efficiency': 0.88,
        },
        'trade_shows': {
            'cost_per_lead': 250,
            'conversion_rate': 0.22,  # 22% conversion rate
            'avg_customer_value': 5500,
            'reach_efficiency': 0.75,
        }
    }
    
    def calculate_campaign_roi(
        self, 
        channel: str, 
        budget: float,
        custom_conversion_rate: Optional[float] = None,
        custom_customer_value: Optional[float] = None
    ) -> ROIResult:
        """
        Calculate expected ROI for a marketing campaign
        
        Args:
            channel: Marketing channel (e.g., 'linkedin_ads', 'email_marketing')
            budget: Campaign budget in dollars
            custom_conversion_rate: Optional custom conversion rate (0-1)
            custom_customer_value: Optional custom average customer value
            
        Returns:
            ROIResult: Expected campaign performance and ROI
        """
        # Validate channel
        if channel not in self.CHANNEL_DATA:
            raise ValueError(
                f"Unknown channel '{channel}'. "
                f"Available channels: {', '.join(self.CHANNEL_DATA.keys())}"
            )
        
        channel_data = self.CHANNEL_DATA[channel]
        
        # Use custom values if provided
        conversion_rate = custom_conversion_rate or channel_data['conversion_rate']
        avg_customer_value = custom_customer_value or channel_data['avg_customer_value']
        
        # Calculate effective budget after platform fees
        effective_budget = budget * channel_data['reach_efficiency']
        
        # Calculate expected customers based on channel type
        if 'cpc' in channel_data:
            # CPC-based channels (LinkedIn, Google, Social)
            clicks = effective_budget / channel_data['cpc']
            expected_customers = int(clicks * conversion_rate)
        elif 'cost_per_lead' in channel_data:
            # Lead-based channels (Content, SEO)
            leads = effective_budget / channel_data['cost_per_lead']
            expected_customers = int(leads * conversion_rate)
        elif 'cost_per_send' in channel_data:
            # Email marketing
            sends = effective_budget / channel_data['cost_per_send']
            opens = sends * channel_data['open_rate']
            clicks = opens * channel_data['click_rate']
            expected_customers = int(clicks * conversion_rate)
        elif 'cost_per_attendee' in channel_data:
            # Event-based channels (Webinars, Trade Shows)
            attendees = effective_budget / channel_data['cost_per_attendee']
            expected_customers = int(attendees * conversion_rate)
        else:
            expected_customers = 0
        
        # Ensure at least some customers if budget is reasonable
        if expected_customers == 0 and budget > 100:
            expected_customers = max(1, int(budget / 1000))
        
        # Calculate revenue and ROI
        expected_revenue = expected_customers * avg_customer_value
        roi_amount = expected_revenue - budget
        roi_percentage = (roi_amount / budget * 100) if budget > 0 else 0
        
        cost_per_customer = budget / expected_customers if expected_customers > 0 else budget
        
        return ROIResult(
            channel=channel,
            budget=budget,
            expected_customers=expected_customers,
            expected_revenue=round(expected_revenue, 2),
            roi_percentage=round(roi_percentage, 1),
            cost_per_customer=round(cost_per_customer, 2),
            revenue_per_customer=avg_customer_value
        )
    
    def optimize_budget_allocation(
        self,
        total_budget: float,
        channels: List[str],
        constraints: Optional[Dict[str, Tuple[float, float]]] = None
    ) -> BudgetAllocation:
        """
        Optimize budget allocation across multiple marketing channels
        
        Args:
            total_budget: Total marketing budget to allocate
            channels: List of marketing channels to consider
            constraints: Optional dict of (min_pct, max_pct) constraints per channel
            
        Returns:
            BudgetAllocation: Optimized allocation with projections
        """
        # Validate channels
        for channel in channels:
            if channel not in self.CHANNEL_DATA:
                raise ValueError(
                    f"Unknown channel '{channel}'. "
                    f"Available channels: {', '.join(self.CHANNEL_DATA.keys())}"
                )
        
        # Calculate ROI efficiency score for each channel
        channel_scores = {}
        for channel in channels:
            data = self.CHANNEL_DATA[channel]
            # Score based on conversion rate, customer value, and efficiency
            avg_value = data['avg_customer_value']
            conv_rate = data['conversion_rate']
            efficiency = data['reach_efficiency']
            
            # Composite score (higher is better)
            score = avg_value * conv_rate * efficiency
            channel_scores[channel] = score
        
        # Sort channels by score (descending)
        sorted_channels = sorted(
            channel_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Apply optimization strategy (weighted allocation based on performance)
        allocations = {}
        allocation_percentages = {}
        
        if constraints:
            # Use constraint-based allocation
            allocations = self._allocate_with_constraints(
                total_budget, sorted_channels, constraints
            )
        else:
            # Use performance-weighted allocation with diminishing returns
            allocations = self._allocate_weighted(
                total_budget, sorted_channels, len(channels)
            )
        
        # Calculate percentages
        for channel, amount in allocations.items():
            allocation_percentages[channel] = round(amount / total_budget * 100, 1)
        
        # Project results for each channel
        projected_results = {}
        total_customers = 0
        total_revenue = 0.0
        
        for channel, budget in allocations.items():
            result = self.calculate_campaign_roi(channel, budget)
            projected_results[channel] = result
            total_customers += result.expected_customers
            total_revenue += result.expected_revenue
        
        # Calculate overall ROI
        overall_roi = ((total_revenue - total_budget) / total_budget * 100) if total_budget > 0 else 0
        
        return BudgetAllocation(
            total_budget=total_budget,
            allocations=allocations,
            allocation_percentages=allocation_percentages,
            projected_results=projected_results,
            total_expected_customers=total_customers,
            total_expected_revenue=round(total_revenue, 2),
            overall_roi_percentage=round(overall_roi, 1)
        )
    
    def _allocate_weighted(
        self, 
        total_budget: float, 
        sorted_channels: List[Tuple[str, float]],
        num_channels: int
    ) -> Dict[str, float]:
        """
        Allocate budget using weighted strategy with diminishing returns
        
        Args:
            total_budget: Total budget to allocate
            sorted_channels: Channels sorted by performance score
            num_channels: Number of channels
            
        Returns:
            Dict mapping channel to budget allocation
        """
        allocations = {}
        
        if num_channels == 1:
            # Single channel gets 100%
            allocations[sorted_channels[0][0]] = total_budget
        elif num_channels == 2:
            # Two channels: 70/30 split
            allocations[sorted_channels[0][0]] = total_budget * 0.70
            allocations[sorted_channels[1][0]] = total_budget * 0.30
        elif num_channels == 3:
            # Three channels: 60/30/10 split (optimal diversification)
            allocations[sorted_channels[0][0]] = total_budget * 0.60
            allocations[sorted_channels[1][0]] = total_budget * 0.30
            allocations[sorted_channels[2][0]] = total_budget * 0.10
        else:
            # More channels: use exponential decay
            total_score = sum(score for _, score in sorted_channels)
            weights = []
            
            for i, (channel, score) in enumerate(sorted_channels):
                # Apply exponential decay: each subsequent channel gets less
                decay_factor = 0.7 ** i
                weight = (score / total_score) * decay_factor
                weights.append(weight)
            
            # Normalize weights to sum to 1
            total_weight = sum(weights)
            normalized_weights = [w / total_weight for w in weights]
            
            # Allocate budget
            for i, (channel, _) in enumerate(sorted_channels):
                allocations[channel] = total_budget * normalized_weights[i]
        
        return allocations
    
    def _allocate_with_constraints(
        self,
        total_budget: float,
        sorted_channels: List[Tuple[str, float]],
        constraints: Dict[str, Tuple[float, float]]
    ) -> Dict[str, float]:
        """
        Allocate budget respecting min/max constraints per channel
        
        Args:
            total_budget: Total budget to allocate
            sorted_channels: Channels sorted by performance score
            constraints: Dict of (min_pct, max_pct) per channel
            
        Returns:
            Dict mapping channel to budget allocation
        """
        allocations = {}
        remaining_budget = total_budget
        remaining_channels = [ch for ch, _ in sorted_channels]
        
        # First pass: allocate minimums
        for channel in remaining_channels:
            if channel in constraints:
                min_pct, _ = constraints[channel]
                min_amount = total_budget * (min_pct / 100)
                allocations[channel] = min_amount
                remaining_budget -= min_amount
            else:
                allocations[channel] = 0
        
        # Second pass: distribute remaining budget respecting maximums
        for channel, _ in sorted_channels:
            if remaining_budget <= 0:
                break
            
            if channel in constraints:
                _, max_pct = constraints[channel]
                max_amount = total_budget * (max_pct / 100)
                available = max_amount - allocations[channel]
                
                if available > 0:
                    to_allocate = min(available, remaining_budget * 0.5)
                    allocations[channel] += to_allocate
                    remaining_budget -= to_allocate
        
        # Third pass: distribute any remaining budget proportionally
        if remaining_budget > 0:
            total_current = sum(allocations.values())
            for channel in allocations:
                if total_current > 0:
                    proportion = allocations[channel] / total_current
                    allocations[channel] += remaining_budget * proportion
        
        return allocations


# Create singleton instance
roi_calc = ROICalculator()
