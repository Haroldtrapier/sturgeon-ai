#!/usr/bin/env python3
"""
Marketing Director Agent - Interactive Demo

This interactive demo showcases all capabilities of the Marketing Director Agent,
including strategic planning, campaign generation, and ROI optimization.
"""

import sys
import json
from typing import Dict, Any
from agent_core import MarketingDirectorAgent
from campaign_generator import CampaignGenerator
from roi_calculator import ROICalculator


class MarketingDirectorDemo:
    """Interactive demo for Marketing Director Agent."""
    
    def __init__(self):
        """Initialize the demo with all agent components."""
        self.agent = MarketingDirectorAgent()
        self.campaign_gen = CampaignGenerator()
        self.roi_calc = ROICalculator()
        self.running = True
    
    def run(self):
        """Run the interactive demo."""
        self.print_welcome()
        
        while self.running:
            self.print_menu()
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == '1':
                self.demo_market_analysis()
            elif choice == '2':
                self.demo_strategy_generation()
            elif choice == '3':
                self.demo_campaign_creation()
            elif choice == '4':
                self.demo_multi_channel_campaign()
            elif choice == '5':
                self.demo_roi_calculation()
            elif choice == '6':
                self.demo_budget_optimization()
            elif choice == '7':
                self.demo_audience_analysis()
            elif choice == '8':
                self.demo_interactive_chat()
            elif choice == '9':
                self.running = False
                print("\n👋 Thank you for using Marketing Director Agent!")
            else:
                print("\n❌ Invalid choice. Please try again.")
            
            if self.running and choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                input("\n⏸️  Press Enter to continue...")
    
    def print_welcome(self):
        """Print welcome message."""
        print("=" * 80)
        print("🎯 MARKETING DIRECTOR AI AGENT - INTERACTIVE DEMO")
        print("=" * 80)
        print("\nWelcome! This demo showcases the comprehensive capabilities of your")
        print("AI-powered Marketing Director Agent, including:")
        print("  • Strategic Marketing Planning")
        print("  • Campaign Generation & Management")
        print("  • ROI Analysis & Budget Optimization")
        print("  • Audience Analysis & Targeting")
        print("  • Interactive Marketing Consultation")
        print()
    
    def print_menu(self):
        """Print the main menu."""
        print("\n" + "=" * 80)
        print("MAIN MENU")
        print("=" * 80)
        print("1. 📊 Market Position Analysis")
        print("2. 🎯 Marketing Strategy Generation")
        print("3. 📢 Create Marketing Campaign")
        print("4. 🌐 Multi-Channel Campaign Generator")
        print("5. 💰 Calculate Campaign ROI")
        print("6. ⚡ Budget Optimization")
        print("7. 👥 Target Audience Analysis")
        print("8. 💬 Interactive Chat with Marketing Director")
        print("9. 🚪 Exit")
    
    def demo_market_analysis(self):
        """Demo market position analysis."""
        print("\n" + "=" * 80)
        print("📊 MARKET POSITION ANALYSIS")
        print("=" * 80)
        
        # Example company data
        company_info = {
            'industry': 'Technology',
            'target_market': 'B2B',
            'size': 'medium',
            'market_share': 'emerging',
            'unique_value_prop': 'AI-powered automation solutions'
        }
        
        print("\n📋 Analyzing market position for:")
        print(f"   Industry: {company_info['industry']}")
        print(f"   Market: {company_info['target_market']}")
        print(f"   Company Size: {company_info['size']}")
        print(f"   Market Position: {company_info['market_share']}")
        
        print("\n🔄 Conducting market analysis...")
        analysis = self.agent.analyze_market_position(company_info)
        
        print("\n✅ ANALYSIS RESULTS:")
        print(f"\n🎯 Market Position: {analysis['market_position']}")
        
        print("\n📈 Key Opportunities:")
        for i, opp in enumerate(analysis['opportunities'], 1):
            print(f"   {i}. {opp}")
        
        print("\n⚠️  Challenges:")
        for i, challenge in enumerate(analysis['challenges'], 1):
            print(f"   {i}. {challenge}")
        
        print("\n💪 Competitive Advantages:")
        for i, adv in enumerate(analysis['competitive_advantages'], 1):
            print(f"   {i}. {adv}")
        
        print("\n🎯 Strategic Recommendations:")
        for i, rec in enumerate(analysis['recommended_strategies'], 1):
            print(f"   {i}. {rec}")
    
    def demo_strategy_generation(self):
        """Demo marketing strategy generation."""
        print("\n" + "=" * 80)
        print("🎯 MARKETING STRATEGY GENERATION")
        print("=" * 80)
        
        objectives = [
            "Increase brand awareness by 50%",
            "Generate 1000+ qualified leads",
            "Improve customer engagement"
        ]
        budget = 50000
        timeframe = "quarterly"
        
        print("\n📋 Strategy Parameters:")
        print(f"   Budget: ${budget:,.2f}")
        print(f"   Timeframe: {timeframe}")
        print("\n   Objectives:")
        for i, obj in enumerate(objectives, 1):
            print(f"   {i}. {obj}")
        
        print("\n🔄 Generating comprehensive marketing strategy...")
        strategy = self.agent.generate_marketing_strategy(objectives, budget, timeframe)
        
        print("\n✅ STRATEGY GENERATED:")
        
        print("\n💰 Budget Allocation by Channel:")
        for channel, amount in strategy['channel_mix'].items():
            percentage = (amount / budget) * 100
            print(f"   • {channel.replace('_', ' ').title()}: ${amount:,.2f} ({percentage:.1f}%)")
        
        print("\n🎬 Key Tactics:")
        for i, tactic in enumerate(strategy['tactics'], 1):
            print(f"\n   {i}. {tactic['name']}")
            print(f"      {tactic['description']}")
            print(f"      Channels: {', '.join(tactic['channels'])}")
        
        print("\n📊 Key Performance Indicators (KPIs):")
        for i, kpi in enumerate(strategy['kpis'], 1):
            print(f"   {i}. {kpi['metric']}: {kpi.get('target', 'TBD')}")
        
        print("\n📅 Implementation Timeline:")
        for phase in strategy['timeline']:
            print(f"   • {phase['phase']}: {phase['focus']}")
    
    def demo_campaign_creation(self):
        """Demo campaign creation."""
        print("\n" + "=" * 80)
        print("📢 MARKETING CAMPAIGN CREATION")
        print("=" * 80)
        
        campaign_params = {
            'campaign_name': 'Q4 Product Launch Campaign',
            'objective': 'product_launch',
            'target_audience': {
                'industry': 'Technology',
                'company_size': '50-500 employees',
                'job_titles': ['CTO', 'VP Engineering', 'Product Manager'],
                'description': 'Tech decision makers at mid-size companies'
            },
            'budget': 35000,
            'duration_days': 45
        }
        
        print("\n📋 Campaign Parameters:")
        print(f"   Name: {campaign_params['campaign_name']}")
        print(f"   Objective: {campaign_params['objective']}")
        print(f"   Budget: ${campaign_params['budget']:,.2f}")
        print(f"   Duration: {campaign_params['duration_days']} days")
        
        print("\n🔄 Generating comprehensive campaign...")
        campaign = self.campaign_gen.generate_campaign(**campaign_params)
        
        print("\n✅ CAMPAIGN CREATED:")
        print(f"\n🎯 Campaign ID: {campaign['id']}")
        print(f"📅 Start Date: {campaign['start_date'][:10]}")
        print(f"📅 End Date: {campaign['end_date'][:10]}")
        
        print("\n📺 Selected Channels:")
        for i, channel in enumerate(campaign['channels'], 1):
            print(f"   {i}. {channel.replace('_', ' ').title()}")
        
        print("\n💰 Budget Allocation:")
        for channel, amount in campaign['budget_allocation'].items():
            print(f"   • {channel.replace('_', ' ').title()}: ${amount:,.2f}")
        
        print("\n📝 Key Messages:")
        for i, msg in enumerate(campaign['messaging']['key_messages'], 1):
            print(f"   {i}. {msg}")
        
        print(f"\n🎨 Tone & Voice: {campaign['messaging']['tone_voice']}")
        print(f"📢 Call to Action: {campaign['messaging']['call_to_action']}")
        
        print("\n📊 Campaign KPIs:")
        for kpi in campaign['kpis']:
            print(f"   • {kpi['metric']}: {kpi.get('target', 'TBD')}")
        
        print("\n📅 Campaign Timeline:")
        for phase in campaign['timeline']:
            print(f"\n   {phase['phase']}: {phase['days']}")
            for activity in phase['activities'][:2]:
                print(f"      - {activity}")
    
    def demo_multi_channel_campaign(self):
        """Demo multi-channel campaign generation."""
        print("\n" + "=" * 80)
        print("🌐 MULTI-CHANNEL INTEGRATED CAMPAIGN")
        print("=" * 80)
        
        segments = [
            {
                'name': 'Enterprise',
                'industry': 'Technology',
                'company_size': '1000+ employees',
                'description': 'Large enterprise decision makers'
            },
            {
                'name': 'Mid-Market',
                'industry': 'Technology',
                'company_size': '100-1000 employees',
                'description': 'Growing mid-market companies'
            }
        ]
        
        print("\n📋 Integrated Campaign Parameters:")
        print("   Campaign: Digital Transformation Initiative")
        print("   Total Budget: $100,000")
        print("   Duration: 60 days")
        print(f"   Target Segments: {len(segments)}")
        
        for i, segment in enumerate(segments, 1):
            print(f"\n   Segment {i}: {segment['name']}")
            print(f"      Size: {segment['company_size']}")
        
        print("\n🔄 Generating integrated multi-channel campaign...")
        campaign = self.campaign_gen.generate_multi_channel_campaign(
            campaign_name="Digital Transformation Initiative",
            objectives=['Lead Generation', 'Brand Awareness'],
            target_segments=segments,
            total_budget=100000,
            duration_days=60
        )
        
        print("\n✅ INTEGRATED CAMPAIGN CREATED:")
        print(f"\n🎯 Campaign: {campaign['name']}")
        print(f"💰 Total Budget: ${campaign['total_budget']:,.2f}")
        print(f"📅 Duration: {campaign['duration_days']} days")
        
        print("\n🎯 Objectives:")
        for i, obj in enumerate(campaign['objectives'], 1):
            print(f"   {i}. {obj}")
        
        print("\n👥 Segment Campaigns:")
        for i, seg_campaign in enumerate(campaign['segment_campaigns'], 1):
            print(f"\n   Segment {i}: {seg_campaign['name']}")
            print(f"      Budget: ${seg_campaign['budget']:,.2f}")
            print(f"      Channels: {', '.join(seg_campaign['channels'][:3])}")
        
        print("\n🔗 Cross-Channel Strategy:")
        strategy = campaign['cross_channel_strategy']
        print(f"   Attribution Model: {strategy['attribution_model']}")
        print(f"   Budget Flexibility: {strategy['budget_flexibility']}")
        
        print("\n📊 Integrated KPIs:")
        for kpi in campaign['integrated_kpis']:
            print(f"   • {kpi['metric']}: {kpi['target']}")
    
    def demo_roi_calculation(self):
        """Demo ROI calculation."""
        print("\n" + "=" * 80)
        print("💰 CAMPAIGN ROI CALCULATION")
        print("=" * 80)
        
        campaign_data = {
            'id': 'camp_123',
            'name': 'Summer Lead Gen Campaign',
            'total_budget': 25000
        }
        
        results_data = {
            'revenue': 95000,
            'leads': 500,
            'customers': 75,
            'avg_customer_value': 1800
        }
        
        print("\n📋 Campaign Data:")
        print(f"   Campaign: {campaign_data['name']}")
        print(f"   Investment: ${campaign_data['total_budget']:,.2f}")
        
        print("\n📊 Campaign Results:")
        print(f"   Revenue Generated: ${results_data['revenue']:,.2f}")
        print(f"   Leads: {results_data['leads']}")
        print(f"   Customers: {results_data['customers']}")
        print(f"   Avg Customer Value: ${results_data['avg_customer_value']:,.2f}")
        
        print("\n🔄 Calculating ROI metrics...")
        roi_analysis = self.roi_calc.calculate_campaign_roi(campaign_data, results_data)
        
        print("\n✅ ROI ANALYSIS:")
        print(f"\n💰 ROI: {roi_analysis['roi_percentage']:.1f}%")
        print(f"📈 ROAS: {roi_analysis['roas']:.2f}x")
        print(f"💵 Cost per Lead: ${roi_analysis['cost_per_lead']:.2f}")
        print(f"💵 Cost per Acquisition: ${roi_analysis['cost_per_acquisition']:.2f}")
        print(f"📊 LTV:CAC Ratio: {roi_analysis['ltv_to_cac_ratio']:.2f}:1")
        print(f"🎯 Performance Grade: {roi_analysis['performance_grade']}")
        
        print("\n💡 Key Insights:")
        for i, insight in enumerate(roi_analysis['insights'], 1):
            print(f"   {i}. {insight}")
        
        print("\n🎯 Recommendations:")
        for i, rec in enumerate(roi_analysis['recommendations'][:3], 1):
            print(f"   {i}. {rec}")
    
    def demo_budget_optimization(self):
        """Demo budget optimization."""
        print("\n" + "=" * 80)
        print("⚡ BUDGET OPTIMIZATION")
        print("=" * 80)
        
        total_budget = 75000
        channels = ['email', 'social_media', 'content', 'paid_ads', 'seo']
        
        # Historical performance data
        historical_performance = {
            'email': {'roi_percentage': 320, 'spend': 8000, 'revenue': 33600},
            'social_media': {'roi_percentage': 180, 'spend': 12000, 'revenue': 33600},
            'content': {'roi_percentage': 250, 'spend': 10000, 'revenue': 35000},
            'paid_ads': {'roi_percentage': 210, 'spend': 20000, 'revenue': 62000},
            'seo': {'roi_percentage': 380, 'spend': 5000, 'revenue': 24000}
        }
        
        print("\n📋 Optimization Parameters:")
        print(f"   Total Budget: ${total_budget:,.2f}")
        print(f"   Channels: {len(channels)}")
        
        print("\n📊 Historical Performance:")
        for channel, perf in historical_performance.items():
            print(f"   • {channel.replace('_', ' ').title()}: ROI {perf['roi_percentage']}%")
        
        print("\n🔄 Optimizing budget allocation...")
        optimization = self.roi_calc.optimize_budget_allocation(
            total_budget=total_budget,
            channels=channels,
            historical_performance=historical_performance,
            objectives=['Lead Generation', 'Revenue Growth']
        )
        
        print("\n✅ OPTIMIZED ALLOCATION:")
        
        print("\n💰 Recommended Budget by Channel:")
        for channel, amount in optimization['recommended_allocation'].items():
            percentage = optimization['allocation_percentages'][channel]
            print(f"   • {channel.replace('_', ' ').title()}: ${amount:,.2f} ({percentage}%)")
        
        print("\n📈 Expected Returns:")
        returns = optimization['expected_returns']
        print(f"   Total Investment: ${returns['total_investment']:,.2f}")
        print(f"   Expected Revenue: ${returns['expected_revenue']:,.2f}")
        print(f"   Expected ROI: {returns['total_roi']:.1f}%")
        print(f"   Confidence: {returns['confidence'].title()}")
        
        print(f"\n🧪 Testing Budget: ${optimization['testing_budget']:,.2f}")
        print(f"📊 Confidence Level: {optimization['confidence_level']}")
        
        print("\n💡 Optimization Rationale:")
        print(f"   {optimization['rationale']}")
    
    def demo_audience_analysis(self):
        """Demo target audience analysis."""
        print("\n" + "=" * 80)
        print("👥 TARGET AUDIENCE ANALYSIS")
        print("=" * 80)
        
        audience_data = {
            'industry': 'Technology',
            'age_range': '30-50',
            'location': 'United States',
            'job_titles': ['CTO', 'VP Engineering', 'Director of IT'],
            'company_size': '100-1000 employees',
            'interests': ['Cloud Computing', 'AI/ML', 'Automation'],
            'loyalty': 'Medium'
        }
        
        print("\n📋 Audience Data:")
        print(f"   Industry: {audience_data['industry']}")
        print(f"   Age Range: {audience_data['age_range']}")
        print(f"   Location: {audience_data['location']}")
        print(f"   Company Size: {audience_data['company_size']}")
        
        print("\n🔄 Analyzing target audience...")
        analysis = self.campaign_gen.analyze_target_audience(audience_data)
        
        print("\n✅ AUDIENCE ANALYSIS:")
        
        print("\n👤 Demographics:")
        demo = analysis['demographics']
        for key, value in demo.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        print("\n🧠 Psychographics:")
        psycho = analysis['psychographics']
        print(f"   Values: {', '.join(psycho['values'])}")
        print(f"   Lifestyle: {psycho['lifestyle']}")
        print(f"   Personality: {psycho['personality']}")
        
        print("\n🎯 Audience Segments:")
        for segment in analysis['segments']:
            print(f"\n   {segment['name']} ({segment['size']})")
            print(f"      {segment['characteristics']}")
            print(f"      Priority: {segment['priority']}")
        
        print("\n👥 Buyer Personas:")
        for persona in analysis['personas']:
            print(f"\n   {persona['name']} - {persona['role']}")
            print(f"      Goals: {', '.join(persona['goals'][:2])}")
            print(f"      Channels: {', '.join(persona['preferred_channels'])}")
        
        print("\n📺 Channel Preferences:")
        prefs = analysis['channel_preferences']
        print(f"   Primary: {prefs['primary']}")
        print(f"   Secondary: {prefs['secondary']}")
        
        print("\n⚠️  Key Pain Points:")
        for i, pain in enumerate(analysis['pain_points'][:3], 1):
            print(f"   {i}. {pain}")
    
    def demo_interactive_chat(self):
        """Demo interactive chat with marketing director."""
        print("\n" + "=" * 80)
        print("💬 INTERACTIVE CHAT WITH MARKETING DIRECTOR AI")
        print("=" * 80)
        print("\nChat with your AI Marketing Director! (Type 'back' to return to main menu)")
        print("Try asking about: strategy, campaigns, budgets, ROI, channels, etc.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['back', 'exit', 'quit', 'menu']:
                break
            
            response = self.agent.chat(user_input)
            print(f"\n🤖 Marketing Director: {response}\n")
    
    def print_section_header(self, title: str):
        """Print a section header."""
        print(f"\n{'=' * 80}")
        print(title)
        print('=' * 80)


def main():
    """Main entry point for the demo."""
    demo = MarketingDirectorDemo()
    
    try:
        demo.run()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thank you for using Marketing Director Agent!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please try again or contact support.")
        sys.exit(1)


if __name__ == "__main__":
    main()
