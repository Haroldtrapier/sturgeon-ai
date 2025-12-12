#!/usr/bin/env python3
"""
Example usage of the Marketing Director Agent

This script demonstrates how to integrate and use the marketing director agent
in your own applications.
"""

from agent_core import MarketingDirectorAgent
from campaign_generator import CampaignGenerator
from roi_calculator import ROICalculator


def example_1_simple_campaign():
    """Example 1: Create a simple marketing campaign"""
    print("\n" + "=" * 70)
    print("Example 1: Creating a Simple Marketing Campaign")
    print("=" * 70)
    
    # Initialize the campaign generator
    generator = CampaignGenerator()
    
    # Create a campaign
    campaign = generator.generate_campaign(
        campaign_name='Q1 Lead Generation Campaign',
        objective='lead_generation',
        target_audience={
            'industry': 'Technology',
            'company_size': '50-500 employees',
            'job_titles': ['Marketing Director', 'CMO', 'VP Marketing']
        },
        budget=25000,
        duration_days=45
    )
    
    print(f"\nCampaign Created: {campaign['name']}")
    print(f"Budget: ${campaign['budget']:,.0f}")
    print(f"Channels: {', '.join(campaign['channels'])}")
    print(f"\nBudget Allocation:")
    for channel, amount in campaign['budget_allocation'].items():
        print(f"  {channel}: ${amount:,.0f}")


def example_2_roi_analysis():
    """Example 2: Calculate ROI for a completed campaign"""
    print("\n" + "=" * 70)
    print("Example 2: Calculating Campaign ROI")
    print("=" * 70)
    
    # Initialize the calculator
    calculator = ROICalculator()
    
    # Campaign data
    campaign_data = {
        'id': 'camp_001',
        'name': 'Product Launch Campaign',
        'total_budget': 40000
    }
    
    # Results data
    results_data = {
        'revenue': 160000,
        'leads': 800,
        'customers': 120,
        'avg_customer_value': 1500
    }
    
    # Calculate ROI
    roi_analysis = calculator.calculate_campaign_roi(campaign_data, results_data)
    
    print(f"\nCampaign: {roi_analysis['campaign_name']}")
    print(f"Investment: ${roi_analysis['total_investment']:,.0f}")
    print(f"Revenue: ${roi_analysis['revenue_generated']:,.0f}")
    print(f"ROI: {roi_analysis['roi_percentage']:.1f}%")
    print(f"ROAS: {roi_analysis['roas']:.2f}x")
    print(f"Performance Grade: {roi_analysis['performance_grade']}")
    
    print("\nKey Insights:")
    for insight in roi_analysis['insights']:
        print(f"  • {insight}")


def example_3_budget_optimization():
    """Example 3: Optimize marketing budget allocation"""
    print("\n" + "=" * 70)
    print("Example 3: Optimizing Marketing Budget")
    print("=" * 70)
    
    # Initialize the calculator
    calculator = ROICalculator()
    
    # Historical performance data
    historical_performance = {
        'email': {'roi_percentage': 280, 'spend': 5000},
        'social_media': {'roi_percentage': 150, 'spend': 8000},
        'content': {'roi_percentage': 320, 'spend': 7000},
        'paid_ads': {'roi_percentage': 200, 'spend': 15000}
    }
    
    # Optimize budget
    optimization = calculator.optimize_budget_allocation(
        total_budget=60000,
        channels=['email', 'social_media', 'content', 'paid_ads'],
        historical_performance=historical_performance,
        objectives=['Lead Generation']
    )
    
    print(f"\nTotal Budget: ${optimization['total_budget']:,.0f}")
    print(f"Expected ROI: {optimization['expected_roi']:.1f}%")
    print("\nRecommended Allocation:")
    for channel, amount in optimization['recommended_allocation'].items():
        percentage = optimization['allocation_percentages'][channel]
        print(f"  {channel}: ${amount:,.0f} ({percentage}%)")


def example_4_strategic_planning():
    """Example 4: Generate marketing strategy"""
    print("\n" + "=" * 70)
    print("Example 4: Strategic Marketing Planning")
    print("=" * 70)
    
    # Initialize the agent
    agent = MarketingDirectorAgent()
    
    # Generate strategy
    strategy = agent.generate_marketing_strategy(
        objectives=[
            'Increase brand awareness by 40%',
            'Generate 500 qualified leads',
            'Improve customer engagement'
        ],
        budget=75000,
        timeframe='quarterly'
    )
    
    print(f"\nStrategy Timeframe: {strategy['timeframe']}")
    print(f"Budget: ${strategy['budget']:,.0f}")
    
    print("\nObjectives:")
    for i, obj in enumerate(strategy['objectives'], 1):
        print(f"  {i}. {obj}")
    
    print("\nChannel Mix:")
    for channel, amount in list(strategy['channel_mix'].items())[:4]:
        print(f"  {channel}: ${amount:,.0f}")
    
    print("\nKey Tactics:")
    for i, tactic in enumerate(strategy['tactics'][:2], 1):
        print(f"  {i}. {tactic['name']}")


def example_5_interactive_chat():
    """Example 5: Interactive chat with the agent"""
    print("\n" + "=" * 70)
    print("Example 5: Interactive Chat with Marketing Director")
    print("=" * 70)
    
    # Initialize the agent
    agent = MarketingDirectorAgent()
    
    # Example conversation
    questions = [
        "What's the best way to allocate a $50k budget?",
        "How can I improve my lead generation campaign?",
        "What ROI should I expect from email marketing?"
    ]
    
    for question in questions[:2]:
        print(f"\nQ: {question}")
        response = agent.chat(question)
        print(f"A: {response[:200]}...")


def example_6_audience_analysis():
    """Example 6: Analyze target audience"""
    print("\n" + "=" * 70)
    print("Example 6: Target Audience Analysis")
    print("=" * 70)
    
    # Initialize generator
    generator = CampaignGenerator()
    
    # Audience data
    audience_data = {
        'industry': 'SaaS',
        'age_range': '28-45',
        'location': 'United States',
        'job_titles': ['Marketing Manager', 'Marketing Director', 'CMO'],
        'company_size': '50-500 employees',
        'interests': ['Marketing Technology', 'Analytics', 'Growth Hacking']
    }
    
    # Analyze audience
    analysis = generator.analyze_target_audience(audience_data)
    
    print("\nDemographics:")
    for key, value in analysis['demographics'].items():
        print(f"  {key}: {value}")
    
    print("\nAudience Segments:")
    for segment in analysis['segments']:
        print(f"  • {segment['name']} ({segment['size']}): {segment['characteristics']}")
    
    print("\nBuyer Personas:")
    for persona in analysis['personas']:
        print(f"  • {persona['name']} - {persona['role']}")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("MARKETING DIRECTOR AGENT - USAGE EXAMPLES")
    print("=" * 70)
    
    examples = [
        example_1_simple_campaign,
        example_2_roi_analysis,
        example_3_budget_optimization,
        example_4_strategic_planning,
        example_5_interactive_chat,
        example_6_audience_analysis
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in {example.__name__}: {e}")
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70)
    print("\nFor interactive demo, run: python marketing_director_demo.py")
    print()


if __name__ == "__main__":
    main()
