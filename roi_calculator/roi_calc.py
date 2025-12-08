"""ROI Calculator module for calculating marketing campaign ROI."""

from typing import Dict, Any


# Channel-specific conversion and revenue metrics
CHANNEL_METRICS = {
    "linkedin_ads": {
        "conversion_rate": 0.0036,  # 0.36% conversion rate
        "average_customer_value": 2388.0,  # Average revenue per customer
    }
}


def calculate_campaign_roi(channel: str, budget: float) -> Dict[str, Any]:
    """
    Calculate ROI for a marketing campaign.
    
    Args:
        channel: Marketing channel name (e.g., "linkedin_ads")
        budget: Campaign budget in dollars
        
    Returns:
        Dictionary containing:
        - customers: Expected number of customers
        - revenue: Expected revenue in dollars
        - roi: Return on investment as a percentage
        
    Raises:
        ValueError: If channel is not supported
    """
    if channel not in CHANNEL_METRICS:
        raise ValueError(f"Unsupported channel: {channel}")
    
    metrics = CHANNEL_METRICS[channel]
    conversion_rate = metrics["conversion_rate"]
    customer_value = metrics["average_customer_value"]
    
    # Calculate expected customers based on conversion rate
    # customers = budget * conversion_rate
    expected_customers = int(budget * conversion_rate)
    
    # Calculate expected revenue
    expected_revenue = expected_customers * customer_value
    
    # Calculate ROI percentage
    roi_percentage = ((expected_revenue - budget) / budget) * 100
    
    return {
        "customers": expected_customers,
        "revenue": expected_revenue,
        "roi": round(roi_percentage, 1)
    }
