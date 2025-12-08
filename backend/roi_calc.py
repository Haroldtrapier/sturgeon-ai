"""
backend/roi_calc.py
ROI Calculator for optimizing marketing budget allocation
"""

from typing import Dict, List, Optional


class ROICalculator:
    """
    ROI Calculator for optimizing budget allocation across marketing channels
    """
    
    # Default allocation percentages for each channel type
    DEFAULT_ALLOCATIONS = {
        'linkedin_ads': 0.60,
        'content_marketing': 0.30,
        'email_marketing': 0.10,
    }
    
    def __init__(self):
        """Initialize the ROI Calculator"""
        self.allocation_strategy = self.DEFAULT_ALLOCATIONS.copy()
    
    def optimize_budget_allocation(
        self,
        total_budget: float,
        channels: List[str],
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, float]:
        """
        Optimize budget allocation across marketing channels
        
        Args:
            total_budget: Total budget to allocate
            channels: List of channel names to allocate budget to
            custom_weights: Optional custom allocation weights (must sum to 1.0)
        
        Returns:
            Dictionary mapping channel names to allocated budget amounts
        
        Example:
            >>> roi_calc = ROICalculator()
            >>> allocation = roi_calc.optimize_budget_allocation(
            ...     total_budget=10000,
            ...     channels=["linkedin_ads", "content_marketing", "email_marketing"]
            ... )
            >>> # Returns: {'linkedin_ads': 6000.0, 'content_marketing': 3000.0, 'email_marketing': 1000.0}
        """
        if total_budget <= 0:
            raise ValueError("Total budget must be positive")
        
        if not channels:
            raise ValueError("At least one channel must be specified")
        
        # Use custom weights if provided, otherwise use default allocation strategy
        weights = custom_weights if custom_weights else self.allocation_strategy
        
        # Calculate allocation for each channel
        allocation = {}
        total_weight = 0.0
        
        # First pass: calculate weights for requested channels
        for channel in channels:
            if channel in weights:
                allocation[channel] = weights[channel]
                total_weight += weights[channel]
            else:
                # If channel not in strategy, assign equal weight from remaining
                allocation[channel] = 0.0
        
        # Normalize weights if they don't sum to 1.0
        if total_weight > 0:
            for channel in allocation:
                if allocation[channel] > 0:
                    allocation[channel] = (allocation[channel] / total_weight) * total_budget
        else:
            # Equal distribution if no weights found
            equal_share = total_budget / len(channels)
            for channel in channels:
                allocation[channel] = equal_share
        
        return allocation
    
    def set_allocation_strategy(self, strategy: Dict[str, float]) -> None:
        """
        Set custom allocation strategy
        
        Args:
            strategy: Dictionary mapping channel names to allocation percentages (0-1)
        
        Raises:
            ValueError: If percentages don't sum to approximately 1.0
        """
        total = sum(strategy.values())
        if not (0.99 <= total <= 1.01):  # Allow small floating point errors
            raise ValueError(f"Allocation percentages must sum to 1.0, got {total}")
        
        self.allocation_strategy = strategy.copy()
    
    def calculate_roi(
        self,
        channel: str,
        investment: float,
        revenue: float
    ) -> float:
        """
        Calculate ROI for a specific channel
        
        Args:
            channel: Channel name
            investment: Amount invested
            revenue: Revenue generated
        
        Returns:
            ROI as a percentage
        """
        if investment <= 0:
            return 0.0
        
        return ((revenue - investment) / investment) * 100
    
    def get_channel_performance(
        self,
        allocations: Dict[str, float],
        historical_roi: Dict[str, float]
    ) -> Dict[str, Dict[str, float]]:
        """
        Project performance based on allocations and historical ROI
        
        Args:
            allocations: Current budget allocations per channel
            historical_roi: Historical ROI percentages per channel
        
        Returns:
            Dictionary with projected revenue and ROI per channel
        """
        performance = {}
        
        for channel, allocation in allocations.items():
            roi_pct = historical_roi.get(channel, 0.0)
            projected_revenue = allocation * (1 + roi_pct / 100)
            
            performance[channel] = {
                'investment': allocation,
                'roi_percentage': roi_pct,
                'projected_revenue': projected_revenue,
                'projected_profit': projected_revenue - allocation
            }
        
        return performance


# Module-level convenience function
def optimize_budget_allocation(
    total_budget: float,
    channels: List[str],
    custom_weights: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Convenience function to optimize budget allocation
    
    Args:
        total_budget: Total budget to allocate
        channels: List of channel names
        custom_weights: Optional custom allocation weights
    
    Returns:
        Dictionary mapping channel names to allocated amounts
    """
    calculator = ROICalculator()
    return calculator.optimize_budget_allocation(total_budget, channels, custom_weights)
