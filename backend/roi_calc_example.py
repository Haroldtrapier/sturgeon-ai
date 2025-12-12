"""
Example usage of the ROI Calculator module

This demonstrates how to use the optimize_budget_allocation function
to allocate marketing budget across different channels.
"""

from roi_calc import ROICalculator, optimize_budget_allocation


def example_basic_usage():
    """Example: Basic budget allocation"""
    print("=" * 60)
    print("Example 1: Basic Budget Allocation")
    print("=" * 60)
    
    # Using the convenience function
    allocation = optimize_budget_allocation(
        total_budget=10000,
        channels=["linkedin_ads", "content_marketing", "email_marketing"]
    )
    
    print(f"\nTotal Budget: $10,000")
    print(f"Allocation Results:")
    for channel, amount in allocation.items():
        percentage = (amount / 10000) * 100
        print(f"  {channel:25s}: ${amount:8,.2f} ({percentage:5.1f}%)")
    # Expected: 60% LinkedIn / 30% Content / 10% Email


def example_custom_weights():
    """Example: Custom allocation weights"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Allocation Weights")
    print("=" * 60)
    
    roi_calc = ROICalculator()
    
    # Set custom allocation strategy
    custom_weights = {
        "linkedin_ads": 0.40,
        "content_marketing": 0.35,
        "email_marketing": 0.25
    }
    
    allocation = roi_calc.optimize_budget_allocation(
        total_budget=15000,
        channels=["linkedin_ads", "content_marketing", "email_marketing"],
        custom_weights=custom_weights
    )
    
    print(f"\nTotal Budget: $15,000")
    print(f"Custom Weights: 40% / 35% / 25%")
    print(f"Allocation Results:")
    for channel, amount in allocation.items():
        percentage = (amount / 15000) * 100
        print(f"  {channel:25s}: ${amount:8,.2f} ({percentage:5.1f}%)")


def example_roi_calculation():
    """Example: Calculate ROI for a campaign"""
    print("\n" + "=" * 60)
    print("Example 3: ROI Calculation")
    print("=" * 60)
    
    roi_calc = ROICalculator()
    
    # Calculate ROI for a LinkedIn campaign
    investment = 5000
    revenue = 12000
    roi = roi_calc.calculate_roi(
        channel="linkedin_ads",
        investment=investment,
        revenue=revenue
    )
    
    print(f"\nLinkedIn Campaign:")
    print(f"  Investment: ${investment:,}")
    print(f"  Revenue:    ${revenue:,}")
    print(f"  ROI:        {roi:.1f}%")
    print(f"  Profit:     ${revenue - investment:,}")


def example_performance_projection():
    """Example: Project performance based on historical data"""
    print("\n" + "=" * 60)
    print("Example 4: Performance Projection")
    print("=" * 60)
    
    roi_calc = ROICalculator()
    
    # Current allocations
    allocations = {
        "linkedin_ads": 6000,
        "content_marketing": 3000,
        "email_marketing": 1000
    }
    
    # Historical ROI data
    historical_roi = {
        "linkedin_ads": 150.0,       # 150% ROI
        "content_marketing": 200.0,   # 200% ROI
        "email_marketing": 100.0      # 100% ROI
    }
    
    performance = roi_calc.get_channel_performance(allocations, historical_roi)
    
    print(f"\nProjected Performance:")
    print(f"{'Channel':<25s} {'Investment':<12s} {'ROI %':<10s} {'Revenue':<12s} {'Profit':<12s}")
    print("-" * 75)
    
    total_investment = 0
    total_revenue = 0
    total_profit = 0
    
    for channel, metrics in performance.items():
        total_investment += metrics['investment']
        total_revenue += metrics['projected_revenue']
        total_profit += metrics['projected_profit']
        
        print(f"{channel:<25s} "
              f"${metrics['investment']:>10,.0f}  "
              f"{metrics['roi_percentage']:>7.0f}%  "
              f"${metrics['projected_revenue']:>10,.0f}  "
              f"${metrics['projected_profit']:>10,.0f}")
    
    print("-" * 75)
    print(f"{'TOTAL':<25s} "
          f"${total_investment:>10,.0f}  "
          f"{((total_revenue - total_investment) / total_investment * 100):>7.0f}%  "
          f"${total_revenue:>10,.0f}  "
          f"${total_profit:>10,.0f}")


if __name__ == "__main__":
    example_basic_usage()
    example_custom_weights()
    example_roi_calculation()
    example_performance_projection()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
