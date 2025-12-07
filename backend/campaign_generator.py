#!/usr/bin/env python3
"""
Campaign Generator Module for Sturgeon AI Marketing Director
Generates LinkedIn outreach campaigns and email nurture sequences
"""


class CampaignGenerator:
    """Marketing campaign generator with pre-built templates and sequences"""
    
    # Configuration constants
    DEMO_BOOKING_RATE = 0.08  # 8% conversion rate for demo bookings
    
    def generate_linkedin_outreach_campaign(self, target_persona, campaign_goal, target_count):
        """
        Generate a complete LinkedIn outreach campaign
        
        Args:
            target_persona: Target audience persona (e.g., 'bd_director')
            campaign_goal: Campaign objective (e.g., 'demo_bookings')
            target_count: Number of targets to reach
            
        Returns:
            dict: Complete campaign structure with sequences, metrics, and execution plan
        """
        campaigns = {
            'bd_director': {
                'campaign_name': 'Government Contracting BD Directors - Demo Booking Campaign',
                'objective': 'Book qualified product demos with BD Directors at government contractors',
                'cadence': {
                    'total_days': 21,
                    'touchpoints': 5
                },
                'target_criteria': {
                    'job_titles': ['Business Development Director', 'BD Manager', 'VP Business Development'],
                    'company_size': '50-500 employees',
                    'industries': ['Defense', 'Aerospace', 'Professional Services', 'IT Services'],
                    'location': 'United States'
                },
                'sequence': [
                    {
                        'day': 1,
                        'type': 'connection',
                        'message': "Hi {first_name},\n\nI noticed your work in business development at {company}. Given your focus on government contracting, I thought you'd be interested in how Sturgeon AI is helping BD teams identify and win more federal opportunities.\n\nWould love to connect and share insights on the latest trends in GovCon BD.\n\nBest,\n[Your Name]"
                    },
                    {
                        'day': 4,
                        'type': 'value_share',
                        'message': "Hi {first_name},\n\nThanks for connecting! I wanted to share something that might be valuable for your team.\n\nWe recently helped a similar-sized contractor increase their qualified opportunity pipeline by 40% using AI-powered contract matching. The key was automating the tedious parts of opportunity discovery so BD teams could focus on relationship building.\n\nI'd be happy to show you how this might work for {company}. Are you open to a brief 15-minute call?\n\nBest,\n[Your Name]"
                    },
                    {
                        'day': 8,
                        'type': 'case_study',
                        'message': "Hi {first_name},\n\nHope you're having a great week! I wanted to follow up and share a quick case study that's relevant to government contractors.\n\nOne of our clients, a mid-size defense contractor, was spending 20+ hours/week manually reviewing SAM.gov. After implementing Sturgeon AI:\n\n✓ 75% reduction in opportunity research time\n✓ 3x increase in qualified bids submitted\n✓ 25% higher win rate on proposals\n\nWould you be open to a 15-minute conversation to see if there's a fit for {company}?\n\nBest,\n[Your Name]"
                    },
                    {
                        'day': 14,
                        'type': 'pain_point',
                        'message': "Hi {first_name},\n\nI know BD directors like yourself often struggle with:\n\n• Too much time on manual opportunity research\n• Missing relevant opportunities in the noise\n• Difficulty prioritizing which pursuits to focus on\n\nDoes any of this resonate with your current challenges?\n\nIf so, I'd love to show you how Sturgeon AI addresses these specific pain points. Would next Tuesday or Wednesday work for a quick call?\n\nBest,\n[Your Name]"
                    },
                    {
                        'day': 21,
                        'type': 'final_touch',
                        'message': "Hi {first_name},\n\nI wanted to reach out one last time before I shift my focus.\n\nIf improving your team's opportunity pipeline and win rates is a priority this quarter, I'd be happy to share how we're helping contractors like {company} achieve measurable results.\n\nIf timing isn't right, totally understand. Feel free to reach out when you're ready to explore this.\n\nBest regards,\n[Your Name]"
                    }
                ],
                'expected_outcomes': {
                    'connection_rate': '35%',
                    'response_rate': '15%',
                    'meeting_booking_rate': '8%',
                    'expected_demos_booked': int(target_count * self.DEMO_BOOKING_RATE)
                },
                'success_metrics': {
                    'connection_acceptance': 0.35,
                    'message_response': 0.15,
                    'demo_booking': self.DEMO_BOOKING_RATE
                },
                'execution_checklist': [
                    'Build target list using Sales Navigator (BD Directors, 50-500 employees, GovCon industry)',
                    'Personalize first connection request with company-specific reference',
                    'Set up automated follow-up sequence in LinkedIn automation tool',
                    'Prepare calendar link and demo deck for quick scheduling',
                    'Track metrics daily: connection rate, response rate, booking rate',
                    'A/B test message variations after first 50 sends',
                    'Follow up with engaged prospects who haven\'t booked yet'
                ]
            }
        }
        
        # Get campaign template based on persona
        if target_persona not in campaigns:
            # Use bd_director as default but this is the only persona currently supported
            target_persona = 'bd_director'
        campaign = campaigns[target_persona]
        
        # Update target count dependent metrics
        campaign['expected_outcomes']['expected_demos_booked'] = int(target_count * self.DEMO_BOOKING_RATE)
        campaign['target_count'] = target_count
        
        return campaign
    
    def generate_email_nurture_sequence(self, segment, goal):
        """
        Generate an email nurture sequence
        
        Args:
            segment: Target segment (e.g., 'free_users')
            goal: Sequence goal (e.g., 'upgrade_to_paid')
            
        Returns:
            dict: Complete email sequence with subject lines, body copy, and metrics
        """
        sequences = {
            'free_users': {
                'campaign_name': 'Free to Paid Conversion Sequence',
                'sequence_type': 'Activation & Upgrade',
                'total_emails': 7,
                'timeline_days': 30,
                'sequence': [
                    {
                        'day': 1,
                        'subject': 'Welcome to Sturgeon AI! Here\'s what to do first',
                        'preview_text': 'Get started with contract matching in under 5 minutes',
                        'body': '''Hi {first_name},

Welcome to Sturgeon AI! We're excited to help you discover and win more government contracts.

Here's how to get the most value in your first week:

Day 1-2: Set up your profile
• Add your company capabilities and past performance
• Configure your opportunity preferences
• Connect your SAM.gov profile

Day 3-5: Explore opportunities
• Review your first 10 AI-matched contracts
• Save interesting opportunities to your pipeline
• Try the proposal compliance checker

Day 6-7: Level up
• Invite your team members (collaboration is key!)
• Set up email alerts for new opportunities
• Explore our proposal template library

Need help? Just reply to this email or schedule a call with our team.

Best,
The Sturgeon AI Team

P.S. Pro users get unlimited contract matching and advanced AI proposal tools. Upgrade anytime in your account settings.'''
                    },
                    {
                        'day': 5,
                        'subject': 'Your first contract matches are ready 🎯',
                        'preview_text': 'We found 15 opportunities that match your capabilities',
                        'body': '''Hi {first_name},

Great news! Our AI has analyzed thousands of federal opportunities and found 15 strong matches for your company.

Here's what makes these opportunities special:

✓ They match your NAICS codes and past performance
✓ They're in your preferred contract size range
✓ Application deadlines are 30-90 days out (perfect timing)

Want to see them? Log in to review your matches: [View Opportunities]

**Success Story:** One of our users found a $2.3M opportunity in their first week that they would have completely missed otherwise. It matched their capabilities perfectly.

Ready to find YOUR perfect opportunity?

Best,
The Sturgeon AI Team

P.S. Free accounts see limited matches. Upgrade to Pro to unlock all opportunities and get priority matching.'''
                    },
                    {
                        'day': 10,
                        'subject': 'How contractors are winning 25% more bids with AI',
                        'preview_text': 'Real results from companies like yours',
                        'body': '''Hi {first_name},

I wanted to share some results we're seeing from government contractors using Sturgeon AI:

📊 The Numbers:
• 75% reduction in opportunity research time
• 3x more qualified bids submitted
• 25% increase in win rates
• Average time saved: 20 hours per week

🎯 What's Working:
1. AI-powered contract matching finds opportunities you'd miss manually
2. Automated compliance checking catches issues before submission
3. Proposal templates save 10+ hours per bid
4. Market intelligence shows you WHO to partner with

The best part? Most contractors see ROI within their first contract win.

Want to see how this would work for your team? I'd be happy to walk you through it: [Schedule Demo]

Best,
The Sturgeon AI Team'''
                    },
                    {
                        'day': 15,
                        'subject': 'You\'re missing out on these opportunities',
                        'preview_text': 'Unlock 47 additional contract matches',
                        'body': '''Hi {first_name},

I noticed you've been exploring opportunities on the free plan. That's great!

But here's what you might not know: There are 47 additional contracts that match your profile that you can't see yet.

Why? The free plan limits you to basic matches. Pro unlocks:

🔓 Advanced matching algorithms
🔓 All opportunity types (contracts, grants, partnerships)
🔓 Historical win/loss analysis
🔓 Competitor intelligence
🔓 Unlimited proposal tools
🔓 Team collaboration features

Many contractors tell us they found their next big contract in the "Pro-only" matches.

Ready to unlock everything? Upgrade to Pro today: [Upgrade Now]

30-day money-back guarantee. No questions asked.

Best,
The Sturgeon AI Team'''
                    },
                    {
                        'day': 20,
                        'subject': 'Special offer: Save 20% on Pro (expires soon)',
                        'preview_text': 'Limited-time discount for early users',
                        'body': '''Hi {first_name},

As an early Sturgeon AI user, I wanted to offer you something special:

🎁 20% OFF your first 3 months of Pro
Code: EARLY20

This is a limited-time offer for users who've shown interest in unlocking the full platform.

Here's what you'll get with Pro:

✅ Unlimited AI contract matching
✅ Advanced proposal generation
✅ Compliance checking & risk scoring
✅ Market intelligence & competitor tracking
✅ Priority customer support
✅ Team collaboration tools

The average Pro user finds 3-5 highly qualified opportunities per month they would have missed otherwise.

Ready to level up your BD game?

[Upgrade with 20% discount] → Code: EARLY20

Offer expires in 5 days.

Best,
The Sturgeon AI Team

P.S. This offer won't last long. Lock in your discount now!'''
                    },
                    {
                        'day': 25,
                        'subject': 'Last chance to save 20% (expires tonight)',
                        'preview_text': 'Your discount code expires at midnight',
                        'body': '''Hi {first_name},

Quick reminder: Your 20% discount on Sturgeon AI Pro expires TONIGHT at midnight.

This is your last chance to:
• Unlock all contract matches (47 waiting for you)
• Get unlimited proposal assistance
• Access advanced market intelligence
• Save 20% for 3 months

Don't miss out on opportunities because of limited access.

[Claim your 20% discount now] → Code: EARLY20

Questions? Just reply to this email.

Best,
The Sturgeon AI Team

P.S. After tonight, this offer won't be available again.'''
                    },
                    {
                        'day': 30,
                        'subject': 'We\'d love your feedback',
                        'preview_text': 'Help us improve Sturgeon AI',
                        'body': '''Hi {first_name},

I hope you've found value in Sturgeon AI so far!

I wanted to personally reach out to ask: What would make Sturgeon AI more valuable for you?

Whether you've upgraded to Pro or you're still on the free plan, your feedback matters.

Would you be open to a quick 10-minute call? I'd love to hear:
• What's working well for you
• What could be better
• What features you wish we had

[Schedule a feedback call] - Pick any time that works for you

As a thank you, I'll give you a free month of Pro (regardless of whether you're a current Pro user or not).

Looking forward to hearing from you!

Best,
[Your Name]
Customer Success, Sturgeon AI

P.S. If you have any questions about government contracting or need help with the platform, I'm here to help.'''
                    }
                ],
                'success_metrics': {
                    'email_open_rate': 0.45,
                    'click_through_rate': 0.12,
                    'conversion_to_paid': 0.08
                },
                'a_b_test_variables': [
                    'Subject line length (short vs. long)',
                    'Discount amount (20% vs. 30%)',
                    'Call-to-action placement (top vs. bottom)',
                    'Social proof inclusion (with vs. without testimonials)',
                    'Urgency timing (3 days vs. 5 days expiration)'
                ]
            }
        }
        
        sequence = sequences.get(segment, sequences['free_users'])
        sequence['segment'] = segment
        sequence['goal'] = goal
        
        return sequence


# Create singleton instance for import
campaign_gen = CampaignGenerator()
