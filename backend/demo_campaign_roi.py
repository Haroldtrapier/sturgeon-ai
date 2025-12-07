#!/usr/bin/env python
"""
Demo script showing the LinkedIn Campaign Generator and ROI Calculator functionality
"""

def main():
    print("=" * 70)
    print("LinkedIn Campaign Generator & ROI Calculator Demo")
    print("=" * 70)
    print()
    
    # Example 1: Generate LinkedIn campaign
    print("1. Generate LinkedIn campaign")
    print("-" * 70)
    print("from campaign_generator import campaign_gen")
    print('campaign = campaign_gen.generate_linkedin_outreach_campaign(')
    print('    target_persona="bd_director",')
    print('    target_count=100')
    print(')')
    print()
    
    from campaign_generator import campaign_gen
    campaign = campaign_gen.generate_linkedin_outreach_campaign(
        target_persona="bd_director",
        target_count=100
    )
    
    print("Returns:")
    print(f"  Campaign: {campaign.campaign_name}")
    print(f"  Messages: {len(campaign.messages)} message sequence")
    print(f"  Targeting: {len(campaign.targeting.job_titles)} job titles, "
          f"{len(campaign.targeting.industries)} industries")
    print(f"  Metrics: {campaign.metrics.expected_response_rate:.1%} response rate, "
          f"{campaign.metrics.estimated_responses} expected responses")
    print()
    
    # Example 2: Calculate ROI
    print("2. Calculate ROI")
    print("-" * 70)
    print("from roi_calculator import roi_calc")
    print('roi = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)')
    print()
    
    from roi_calculator import roi_calc
    roi = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)
    
    print("Returns:")
    print(f"  Expected customers: {roi.expected_customers}")
    print(f"  Revenue: ${roi.expected_revenue:,.0f}")
    print(f"  ROI: {roi.roi_percentage:.1f}%")
    print()
    
    # Example 3: Optimize budget
    print("3. Optimize budget")
    print("-" * 70)
    print("allocation = roi_calc.optimize_budget_allocation(10000,")
    print('    ["linkedin_ads", "content_marketing", "email_marketing"]')
    print(')')
    print()
    
    allocation = roi_calc.optimize_budget_allocation(
        10000, 
        ["linkedin_ads", "content_marketing", "email_marketing"]
    )
    
    print("Returns:")
    print("  Optimal allocation:")
    for channel, amount in allocation.allocations.items():
        pct = allocation.allocation_percentages[channel]
        print(f"    {channel}: ${amount:,.0f} ({pct:.0f}%)")
    
    print()
    print("  Projections:")
    print(f"    Total customers: {allocation.total_expected_customers}")
    print(f"    Total revenue: ${allocation.total_expected_revenue:,.0f}")
    print(f"    Overall ROI: {allocation.overall_roi_percentage:.1f}%")
    print()
    
    print("=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
