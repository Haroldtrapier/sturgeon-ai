"""
CAMPAIGN GENERATOR MODULE
Generates marketing campaigns for various channels and personas
"""


class CampaignGenerator:
    """Generate marketing campaigns with realistic content and metrics"""
    
    def __init__(self):
        self.personas = {
            'bd_director': {
                'title': 'Business Development Director',
                'industries': ['Government Contracting', 'Defense', 'Professional Services'],
                'pain_points': [
                    'Finding qualified opportunities',
                    'Proposal writing efficiency',
                    'Compliance complexity',
                    'Competitive intelligence'
                ],
                'job_levels': ['Director', 'VP', 'C-Level']
            }
        }
        
        self.email_segments = {
            'free_users': {
                'description': 'Users on free plan for 7+ days',
                'size': 1000,
                'engagement_level': 'medium'
            }
        }
    
    def generate_linkedin_outreach_campaign(self, target_persona, campaign_goal, target_count):
        """
        Generate a complete LinkedIn outreach campaign
        
        Args:
            target_persona: Target audience persona (e.g., 'bd_director')
            campaign_goal: Campaign objective (e.g., 'demo_bookings')
            target_count: Number of prospects to target
            
        Returns:
            Complete campaign dictionary with sequences, metrics, and execution plan
        """
        persona = self.personas.get(target_persona, self.personas['bd_director'])
        
        # Generate message sequence
        sequence = [
            {
                'day': 0,
                'type': 'connection_request',
                'message': f"Hi [First Name],\n\nI noticed your work in {persona['industries'][0]} and thought we should connect. We're helping BD leaders like you streamline the proposal process with AI.\n\nWould love to share some insights on how teams are cutting proposal time by 60%.\n\nBest,\n[Your Name]"
            },
            {
                'day': 3,
                'type': 'follow_up',
                'message': f"Hi [First Name],\n\nThanks for connecting! I wanted to share a quick case study - one of our clients in {persona['industries'][0]} reduced their proposal turnaround from 3 weeks to 5 days using our AI platform.\n\nThey're now winning 40% more contracts. Would you be open to a 15-min call to see if we could help your team achieve similar results?\n\nBest,\n[Your Name]"
            },
            {
                'day': 7,
                'type': 'value_share',
                'message': f"Hi [First Name],\n\nI came across this article on federal contracting trends and thought of you: [Link]\n\nOne stat that stood out: 73% of contractors say compliance is their #1 bottleneck. Our platform automates compliance checking, which might be relevant for your team.\n\nLet me know if you'd like to see how it works.\n\nBest,\n[Your Name]"
            },
            {
                'day': 14,
                'type': 'case_study',
                'message': f"Hi [First Name],\n\nQuick question - are you currently using any AI tools to help with proposal writing or opportunity matching?\n\nWe just helped a {persona['industries'][0]} firm increase their win rate from 18% to 31% in 6 months. Happy to show you their approach if you're interested.\n\nBest,\n[Your Name]"
            },
            {
                'day': 21,
                'type': 'final_touchpoint',
                'message': f"Hi [First Name],\n\nI know you're busy, so I'll keep this brief. We have a new AI feature that automatically identifies the best-fit opportunities for your team based on past wins.\n\nWould you be interested in a quick 10-minute demo? I can show you opportunities we'd recommend for your company.\n\nLet me know if next week works.\n\nBest,\n[Your Name]"
            }
        ]
        
        return {
            'campaign_name': f'LinkedIn Outreach - {persona["title"]}s - {campaign_goal.replace("_", " ").title()}',
            'objective': campaign_goal.replace('_', ' ').title(),
            'target_persona': persona,
            'target_criteria': {
                'job_titles': persona['job_levels'],
                'industries': persona['industries'],
                'company_size': ['51-200', '201-500', '501-1000', '1000+'],
                'geography': ['United States']
            },
            'cadence': {
                'total_days': 21,
                'touchpoints': 5,
                'messages_per_week': '2-3'
            },
            'sequence': sequence,
            'expected_outcomes': {
                'connection_rate': '30-40%',
                'response_rate': '10-15%',
                'meeting_bookings': '5-8%',
                'estimated_meetings': max(3, int(target_count * 0.06))
            },
            'success_metrics': {
                'connection_acceptance': 0.35,
                'response_rate': 0.12,
                'meeting_booking_rate': 0.06,
                'show_up_rate': 0.75
            },
            'execution_checklist': [
                'Export target list from LinkedIn Sales Navigator',
                'Personalize first line of each message with company-specific insight',
                'Set up tracking spreadsheet for responses',
                'Schedule follow-up reminders in CRM',
                'Prepare demo environment for booked calls',
                'Create meeting booking link (Calendly/Chili Piper)',
                'Set up automated thank-you message for connections',
                'Monitor response rates and adjust messaging as needed'
            ]
        }
    
    def generate_email_nurture_sequence(self, segment, goal):
        """
        Generate email nurture sequence for converting users
        
        Args:
            segment: Target user segment (e.g., 'free_users')
            goal: Conversion goal (e.g., 'upgrade_to_paid')
            
        Returns:
            Email sequence with subject lines, bodies, and metrics
        """
        segment_data = self.email_segments.get(segment, self.email_segments['free_users'])
        
        emails = [
            {
                'day': 0,
                'subject': 'Welcome to Sturgeon AI - Let\'s get you started',
                'preview_text': 'Here are 3 quick wins you can achieve today',
                'body': """Hi [First Name],

Welcome to Sturgeon AI! We're excited to help you win more government contracts.

Here are 3 things you can do right now to get value:

1. **Search Opportunities** - Use our AI to find contracts that match your past wins
2. **Generate Your First Proposal** - Try our AI proposal writer (saves 10+ hours)
3. **Check Compliance** - Upload a past proposal and get instant compliance feedback

Most users see their first win within 60 days of using these features.

Click here to get started: [Dashboard Link]

Questions? Just reply to this email.

Best,
The Sturgeon AI Team

P.S. - Check out our knowledge base for video tutorials: [Link]"""
            },
            {
                'day': 3,
                'subject': '[First Name], here\'s how to find your best opportunities',
                'preview_text': 'Use AI matching to filter 10,000+ contracts down to your top 10',
                'body': """Hi [First Name],

I wanted to share a quick tip on getting the most value from Sturgeon AI.

Our AI analyzes 10,000+ active federal contracts every day. But here's the secret: the "Smart Match" feature filters these down to the 10-20 opportunities you're most likely to win.

**How it works:**
- Tell us about your past wins (or upload proposals)
- AI learns your sweet spot
- Get daily alerts for matching opportunities

One of our users, a small defense contractor, found 3 qualified opportunities in their first week. They're now bidding on all three.

Try Smart Match here: [Link]

Best,
The Sturgeon AI Team"""
            },
            {
                'day': 7,
                'subject': 'Case Study: How TechGov won $2.4M in contracts',
                'preview_text': 'From 0 to 3 federal contracts in 6 months',
                'body': """Hi [First Name],

I wanted to share a success story from one of our customers.

**TechGov Solutions** started using Sturgeon AI 6 months ago with zero federal contracts. Today they have:
- 3 active federal contracts worth $2.4M
- 18% win rate (industry average is 5-10%)
- 60% faster proposal turnaround

**What they did differently:**

1. Used our AI to identify opportunities that matched their capabilities
2. Generated first-draft proposals in hours (not weeks)
3. Used compliance checker to avoid disqualification
4. Tracked competitor activity through our intel features

You can achieve similar results. The key is using all our tools together.

Want to learn their strategy? We created a 15-minute walkthrough: [Video Link]

Best,
The Sturgeon AI Team"""
            },
            {
                'day': 11,
                'subject': 'Your proposal writing just got 10x faster',
                'preview_text': 'See the AI proposal generator in action',
                'body': """Hi [First Name],

Quick question: How long does it take your team to write a proposal?

If you're like most contractors, it's probably 2-4 weeks.

Our AI Proposal Generator can create a complete first draft in 2-3 hours.

**Here's what it includes:**
✓ Technical approach based on your past wins
✓ Management plan tailored to the RFP
✓ Past performance examples (automatically matched)
✓ Compliance matrix (pre-filled)
✓ Executive summary

You review and refine. The AI does the heavy lifting.

Try it on your next opportunity: [Link]

Best,
The Sturgeon AI Team

P.S. - Pro users get unlimited proposals. Upgrade here: [Link]"""
            },
            {
                'day': 15,
                'subject': '[First Name], unlock the full platform',
                'preview_text': 'Here\'s what you\'re missing on the free plan',
                'body': """Hi [First Name],

You've been using the free version of Sturgeon AI for a couple weeks now. Great!

I wanted to show you what you're missing with a Pro upgrade:

**Free Plan (Current):**
- 10 opportunity searches/month
- 1 AI proposal/month
- Basic compliance checking

**Pro Plan ($149/month):**
✓ Unlimited searches
✓ Unlimited AI proposals
✓ Advanced compliance scanning
✓ Competitor intelligence
✓ Team collaboration
✓ Priority support

**Here's the math:**
If you win just ONE additional contract per year using Pro features, it pays for itself 100x over.

Most of our Pro users report 2-3 additional wins per year.

**Special Offer:** Upgrade this week and get 30% off your first 3 months.

Upgrade now: [Link]

Best,
The Sturgeon AI Team"""
            },
            {
                'day': 20,
                'subject': 'You\'re leaving money on the table',
                'preview_text': 'Pro users win 3x more contracts. Here\'s why.',
                'body': """Hi [First Name],

I'll be direct: our data shows Pro users win 3x more contracts than free users.

Why? Three reasons:

1. **They find more qualified opportunities** (unlimited search)
2. **They submit more proposals** (unlimited AI generation)
3. **They never miss deadlines** (team collaboration + tracking)

Free users average 0.5 wins per year.
Pro users average 2.3 wins per year.

If your average contract is $500K, that's an extra $900K in revenue.

For $149/month.

The ROI is obvious.

**Limited Time:** Get 30% off if you upgrade in the next 48 hours.

Upgrade here: [Link]

Questions? Schedule a call: [Calendly Link]

Best,
The Sturgeon AI Team"""
            },
            {
                'day': 27,
                'subject': 'Last chance: 30% off Pro (expires tonight)',
                'preview_text': 'Final reminder - special pricing ends at midnight',
                'body': """Hi [First Name],

This is your final reminder - our 30% off promotion for Pro ends tonight at midnight.

**What you get:**
✓ Unlimited opportunity search
✓ Unlimited AI proposals
✓ Advanced features
✓ Priority support

**What it costs:**
$149/month → **$104/month** (with 30% off for 3 months)

**What it's worth:**
The average Pro user wins $1.2M more in contracts per year.

This is the last email I'll send about this promotion.

Upgrade before midnight: [Link]

Best,
The Sturgeon AI Team

P.S. - If you have questions, reply to this email or schedule a quick call: [Link]"""
            }
        ]
        
        return {
            'campaign_name': f'Email Nurture - {segment.replace("_", " ").title()} → {goal.replace("_", " ").title()}',
            'sequence_type': 'Drip Campaign',
            'segment': segment_data,
            'total_emails': len(emails),
            'timeline_days': 27,
            'sequence': emails,
            'success_metrics': {
                'open_rate_target': 0.35,
                'click_rate_target': 0.08,
                'conversion_rate_target': 0.05,
                'unsubscribe_rate_max': 0.02
            },
            'a_b_test_variables': [
                'Subject line length (short vs long)',
                'CTA placement (top vs bottom)',
                'Social proof (case study vs testimonial)',
                'Urgency level (high vs low)',
                'Price visibility (show upfront vs click to reveal)'
            ],
            'technical_setup': {
                'email_service': 'SendGrid / Mailchimp / Customer.io',
                'tracking_pixels': 'Enabled',
                'link_tracking': 'Enabled',
                'spam_score_check': 'Required before send',
                'send_time_optimization': 'Enabled (9-11am recipient timezone)'
            }
        }


# Create singleton instance
campaign_gen = CampaignGenerator()
