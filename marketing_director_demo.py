#!/usr/bin/env python3
"""
STURGEON AI MARKETING DIRECTOR - INTERACTIVE DEMO
Run this to see the Marketing Director Agent in action

Usage: python marketing_director_demo.py
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(__file__))

from campaign_generator import campaign_gen
from roi_calculator import roi_calc
import json


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_section(text):
    """Print section divider"""
    print(f"\n--- {text} ---\n")


def demo_linkedin_campaign():
    """Demonstrate LinkedIn outreach campaign generation"""
    print_header("LINKEDIN OUTREACH CAMPAIGN GENERATOR")
    
    print("Generating complete LinkedIn campaign for BD Directors...")
    campaign = campaign_gen.generate_linkedin_outreach_campaign(
        target_persona="bd_director",
        campaign_goal="demo_bookings",
        target_count=100
    )
    
    print_section("Campaign Overview")
    print(f"Campaign Name: {campaign['campaign_name']}")
    print(f"Objective: {campaign['objective']}")
    print(f"Timeline: {campaign['cadence']['total_days']} days")
    print(f"Touchpoints: {campaign['cadence']['touchpoints']}")
    
    print_section("Target Criteria")
    for key, value in campaign['target_criteria'].items():
        if isinstance(value, list):
            print(f"  {key}: {', '.join(value)}")
        else:
            print(f"  {key}: {value}")
    
    print_section("5-Message Sequence (Ready to Use)")
    for i, msg in enumerate(campaign['sequence'], 1):
        print(f"\nMessage {i} (Day {msg['day']}) - {msg['type'].title()}")
        print("-" * 60)
        print(msg['message'])
    
    print_section("Expected Outcomes")
    for key, value in campaign['expected_outcomes'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print_section("Success Metrics")
    for key, value in campaign['success_metrics'].items():
        print(f"  {key.replace('_', ' ').title()}: {value*100:.1f}%")
    
    print_section("Execution Checklist")
    for i, task in enumerate(campaign['execution_checklist'], 1):
        print(f"  {i}. {task}")


def demo_email_nurture():
    """Demonstrate email nurture sequence"""
    print_header("EMAIL NURTURE SEQUENCE GENERATOR")
    
    print("Generating 7-email free-to-paid conversion sequence...")
    sequence = campaign_gen.generate_email_nurture_sequence(
        segment="free_users",
        goal="upgrade_to_paid"
    )
    
    print_section("Sequence Overview")
    print(f"Campaign: {sequence['campaign_name']}")
    print(f"Type: {sequence['sequence_type']}")
    print(f"Total Emails: {sequence['total_emails']}")
    print(f"Timeline: {sequence['timeline_days']} days")
    
    print_section("Email Preview (First 2 Emails)")
    for i, email in enumerate(sequence['sequence'][:2], 1):
        print(f"\nEmail {i} (Day {email['day']})")
        print(f"Subject: {email['subject']}")
        print(f"Preview: {email['preview_text']}")
        print(f"\nBody:\n{email['body'][:500]}...")
        print("\n" + "-" * 60)
    
    print_section("Success Metrics Targets")
    for key, value in sequence['success_metrics'].items():
        print(f"  {key.replace('_', ' ').title()}: {value*100:.1f}%")
    
    print_section("A/B Test Variables")
    for var in sequence['a_b_test_variables']:
        print(f"  • {var}")


def demo_roi_calculator():
    """Demonstrate ROI calculations"""
    print_header("MARKETING ROI CALCULATOR")
    
    print("Calculating ROI for $5,000 LinkedIn Ads campaign...")
    roi = roi_calc.calculate_campaign_roi(
        channel="linkedin_ads",
        budget=5000,
        duration_months=3
    )
    
    print_section("Investment")
    print(f"  Budget: ${roi['investment']['budget']:,.0f}")
    print(f"  Duration: {roi['investment']['duration_months']} months")
    print(f"  Monthly Spend: ${roi['investment']['monthly_spend']:,.0f}")
    
    print_section("Expected Performance")
    for key, value in roi['performance'].items():
        if isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: ${value:,.0f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print_section("Efficiency Metrics")
    for key, value in roi['efficiency_metrics'].items():
        if 'ratio' in key:
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}:1")
        elif 'months' in key:
            print(f"  {key.replace('_', ' ').title()}: {value:.1f} months")
        else:
            print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")
    
    print_section("Returns")
    for key, value in roi['returns'].items():
        if 'percentage' in key:
            print(f"  {key.replace('_', ' ').title()}: {value:.1f}%")
        elif isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: ${value:,.0f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}x")
    
    print_section("Strategic Recommendation")
    print(f"  {roi['recommendation']}")


def demo_budget_optimization():
    """Demonstrate budget allocation optimization"""
    print_header("MULTI-CHANNEL BUDGET OPTIMIZATION")
    
    print("Optimizing $10,000 budget across 3 channels...")
    allocation = roi_calc.optimize_budget_allocation(
        total_budget=10000,
        channels=["linkedin_ads", "content_marketing", "email_marketing"]
    )
    
    print_section("Optimized Allocation")
    for channel, details in allocation['optimized_allocation'].items():
        print(f"\n{channel.replace('_', ' ').title()}:")
        print(f"  Budget: ${details['budget']:,.0f} ({details['percentage']}%)")
        print(f"  Expected Customers: {details['expected_customers']}")
        print(f"  Expected Revenue: ${details['expected_revenue']:,.0f}")
        print(f"  ROI: {details['roi']:.1f}%")
    
    print_section("Total Expected Results")
    for key, value in allocation['total_expected_results'].items():
        if isinstance(value, float) and value > 100:
            print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")
        elif isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: {value:.1f}%")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print_section("Execution Priority")
    for priority in allocation['execution_priority']:
        if priority:
            print(f"  {priority}")


def demo_growth_projection():
    """Demonstrate 12-month growth projection"""
    print_header("12-MONTH GROWTH TRAJECTORY")
    
    print("Projecting growth with $3,000/month marketing budget...")
    projection = roi_calc.project_growth_trajectory(
        monthly_budget=3000,
        duration_months=12
    )
    
    print_section("Configuration")
    print(f"  Monthly Budget: ${projection['monthly_budget']:,.0f}")
    print(f"  Total Investment: ${projection['total_investment']:,.0f}")
    print(f"  Projection Period: {projection['projection_period']}")
    
    print_section("Channel Allocation")
    for channel, percentage in projection['channel_allocation'].items():
        print(f"  {channel.replace('_', ' ').title()}: {percentage*100:.0f}%")
    
    print_section("Quarter-by-Quarter Results")
    for month in [3, 6, 9, 12]:
        month_data = projection['monthly_breakdown'][month-1]
        print(f"\nMonth {month}:")
        print(f"  New Customers: {month_data['customers']}")
        print(f"  Cumulative Customers: {month_data['cumulative_customers']}")
        print(f"  MRR: ${month_data['mrr']:,.0f}")
        print(f"  Cumulative Revenue: ${month_data['cumulative_revenue']:,.0f}")
    
    print_section("Year-End Totals")
    for key, value in projection['year_end_totals'].items():
        if isinstance(value, float):
            if 'roi' in key:
                print(f"  {key.replace('_', ' ').title()}: {value:.1f}%")
            else:
                print(f"  {key.replace('_', ' ').title()}: ${value:,.0f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print_section("Key Milestones")
    for key, value in projection['key_milestones'].items():
        if value > 0:
            print(f"  {key.replace('_', ' ').title()}: Month {value}")
        else:
            print(f"  {key.replace('_', ' ').title()}: Not achieved in projection period")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  STURGEON AI MARKETING DIRECTOR - LIVE DEMO".center(78) + "║")
    print("║" + "  Internal Use Only - Trapier Management LLC".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    
    demos = [
        ("LinkedIn Outreach Campaign", demo_linkedin_campaign),
        ("Email Nurture Sequence", demo_email_nurture),
        ("ROI Calculator", demo_roi_calculator),
        ("Budget Optimization", demo_budget_optimization),
        ("Growth Projection", demo_growth_projection)
    ]
    
    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  {len(demos)+1}. Run All Demos")
    print("  0. Exit")
    
    try:
        choice = input("\nSelect demo (0-6): ").strip()
        
        if choice == "0":
            print("\nExiting...")
            return
        elif choice == str(len(demos)+1):
            for name, demo_func in demos:
                demo_func()
                input("\nPress Enter to continue...")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            demos[int(choice)-1][1]()
        else:
            print("Invalid selection")
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
