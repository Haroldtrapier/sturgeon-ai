#!/usr/bin/env python3
"""
Campaign Generator Module for Sturgeon AI Marketing Director
Generates LinkedIn outreach campaigns and email nurture sequences
"""


class CampaignGenerator:
    """Generate marketing campaigns and email sequences"""
    
    def generate_linkedin_outreach_campaign(self, target_persona, campaign_goal, target_count):
        """
        Generate a complete LinkedIn outreach campaign
        
        Args:
            target_persona: Target audience persona (e.g., "bd_director")
            campaign_goal: Campaign objective (e.g., "demo_bookings")
            target_count: Number of prospects to target
            
        Returns:
            dict: Complete campaign with messages, timeline, and metrics
        """
        # Define persona-specific messaging
        personas = {
            "bd_director": {
                "title": "Business Development Directors",
                "pain_points": ["Manual proposal processes", "Missing opportunities", "Compliance complexity"],
                "industries": ["Defense", "Aerospace", "Consulting", "IT Services"],
                "company_sizes": ["50-500 employees", "500-5000 employees"],
            }
        }
        
        persona_data = personas.get(target_persona, personas["bd_director"])
        
        # Generate 5-message sequence
        messages = [
            {
                "day": 0,
                "type": "connection_request",
                "message": f"Hi {{{{first_name}}}},\n\nI noticed your work in government contracting at {{{{company}}}}. "
                          f"I help {persona_data['title'].lower()} streamline their proposal processes with AI.\n\n"
                          f"Would love to connect and share insights on winning more federal contracts."
            },
            {
                "day": 2,
                "type": "introduction",
                "message": f"Thanks for connecting, {{{{first_name}}}}!\n\n"
                          f"I work with companies like {{{{company}}}} that struggle with {persona_data['pain_points'][0].lower()} "
                          f"and {persona_data['pain_points'][1].lower()}.\n\n"
                          f"Our AI platform has helped contractors increase win rates by 40% while cutting proposal time in half.\n\n"
                          f"Quick question: What's your biggest challenge in the BD process right now?"
            },
            {
                "day": 5,
                "type": "value_proposition",
                "message": f"{{{{first_name}}}}, thought you might find this interesting:\n\n"
                          f"We just helped a {persona_data['industries'][0]} contractor win 3 major IDIQ contracts worth $12M "
                          f"using our AI-powered opportunity matching.\n\n"
                          f"They were spending 80+ hours per proposal. Now it's down to 20 hours with better quality.\n\n"
                          f"Would a 15-minute demo be valuable for your team?"
            },
            {
                "day": 8,
                "type": "social_proof",
                "message": f"{{{{first_name}}}}, I wanted to share this quick win:\n\n"
                          f"One of our clients (similar to {{{{company}}}}) just closed $2.3M in new contracts after using "
                          f"Sturgeon AI for just 3 months.\n\n"
                          f"Their secret? AI-powered compliance checking that eliminated costly mistakes.\n\n"
                          f"Open to a brief conversation about how we could help {{{{company}}}}?"
            },
            {
                "day": 12,
                "type": "breakup",
                "message": f"Hi {{{{first_name}}}},\n\n"
                          f"I haven't heard back, so I'm assuming this isn't a priority right now.\n\n"
                          f"No worries at all! If your situation changes or you want to chat about improving your win rate, "
                          f"feel free to reach out.\n\n"
                          f"Best of luck with your upcoming proposals!"
            }
        ]
        
        campaign = {
            "campaign_name": f"LinkedIn Outreach - {persona_data['title']} - {campaign_goal.replace('_', ' ').title()}",
            "objective": f"Book qualified demos with {target_count} {persona_data['title'].lower()}",
            "target_persona": target_persona,
            "target_count": target_count,
            "target_criteria": {
                "job_titles": ["Director of Business Development", "VP Business Development", "BD Director", "Growth Director"],
                "industries": persona_data["industries"],
                "company_sizes": persona_data["company_sizes"],
                "geography": ["United States", "Washington DC Metro", "Major defense hubs"]
            },
            "cadence": {
                "total_days": 12,
                "touchpoints": 5,
                "channels": ["LinkedIn"]
            },
            "sequence": messages,
            "expected_outcomes": {
                "connection_rate": "35-45%",
                "response_rate": "15-20%",
                "demo_booking_rate": "8-12%",
                "expected_demos": int(target_count * 0.10)
            },
            "success_metrics": {
                "connection_acceptance": 0.40,
                "message_response": 0.18,
                "demo_booking": 0.10,
                "demo_show_rate": 0.75,
                "demo_to_opportunity": 0.40
            },
            "execution_checklist": [
                "Export target list from LinkedIn Sales Navigator",
                "Personalize {{first_name}} and {{company}} variables",
                "Set up automated sequence in outreach tool",
                "Track responses in CRM",
                "Schedule demos within 48 hours of positive response",
                "Follow up with no-shows within 24 hours",
                "Move qualified leads to sales pipeline"
            ]
        }
        
        return campaign
    
    def generate_email_nurture_sequence(self, segment, goal):
        """
        Generate an email nurture sequence
        
        Args:
            segment: Target segment (e.g., "free_users")
            goal: Sequence goal (e.g., "upgrade_to_paid")
            
        Returns:
            dict: Complete email sequence with timing and metrics
        """
        # Define segment-specific content
        segments = {
            "free_users": {
                "name": "Free Tier Users",
                "pain_points": ["Limited features", "Manual work", "Slow processes"],
                "benefits": ["Unlimited access", "AI assistance", "Priority support"]
            }
        }
        
        segment_data = segments.get(segment, segments["free_users"])
        
        # Generate 7-email sequence
        emails = [
            {
                "day": 0,
                "subject": "Welcome to Sturgeon AI! Here's how to get started 🎯",
                "preview_text": "Your guide to winning more government contracts",
                "body": f"Hi {{{{first_name}}}},\n\n"
                       f"Welcome to Sturgeon AI! You've just joined 1,000+ contractors who are winning more federal contracts with AI.\n\n"
                       f"Here's what you can do right now:\n"
                       f"✓ Search 50,000+ active opportunities\n"
                       f"✓ Get AI-powered match recommendations\n"
                       f"✓ Track competitors and past performance\n\n"
                       f"Pro tip: Companies that complete their profile in the first 24 hours are 3x more likely to win opportunities.\n\n"
                       f"Ready to get started? [Complete Your Profile]\n\n"
                       f"Best regards,\n"
                       f"The Sturgeon AI Team",
                "cta": "Complete Your Profile",
                "cta_url": "https://sturgeon.ai/profile/setup"
            },
            {
                "day": 2,
                "subject": "🚀 You're missing out on these powerful features",
                "preview_text": "Upgrade to unlock AI proposal generation",
                "body": f"Hi {{{{first_name}}}},\n\n"
                       f"I noticed you haven't explored our AI Proposal Generator yet.\n\n"
                       f"This is one of our most powerful features. Here's what it can do:\n\n"
                       f"• Generate complete proposal drafts in minutes (not days)\n"
                       f"• Auto-populate compliance matrices\n"
                       f"• Suggest winning past performance examples\n\n"
                       f"Real results: Our customers reduce proposal time by 60% and increase win rates by 40%.\n\n"
                       f"Want to try it? Upgrade to Pro for 14 days free: [Start Free Trial]\n\n"
                       f"Questions? Just reply to this email.\n\n"
                       f"Best,\n"
                       f"Sarah Chen\n"
                       f"Customer Success, Sturgeon AI",
                "cta": "Start Free Trial",
                "cta_url": "https://sturgeon.ai/upgrade?trial=14"
            },
            {
                "day": 5,
                "subject": "Case Study: How TechDefense won $8.5M in contracts",
                "preview_text": "From 2 wins to 7 wins in 6 months",
                "body": f"Hi {{{{first_name}}}},\n\n"
                       f"I wanted to share an inspiring story.\n\n"
                       f"TechDefense, a 50-person IT contractor, was struggling:\n"
                       f"• Submitting 20+ proposals/year with only 2 wins\n"
                       f"• Spending 100+ hours per proposal\n"
                       f"• Missing opportunities due to slow turnaround\n\n"
                       f"After switching to Sturgeon AI Pro:\n"
                       f"✓ Won 7 contracts in 6 months ($8.5M total)\n"
                       f"✓ Cut proposal time from 100 to 35 hours\n"
                       f"✓ Improved win rate from 10% to 35%\n\n"
                       f"Want similar results? [Read Full Case Study]\n\n"
                       f"Their secret? AI-powered compliance checking and proposal automation.\n\n"
                       f"Ready to upgrade? [Start Your Free Trial]\n\n"
                       f"Best,\n"
                       f"Sarah",
                "cta": "Read Full Case Study",
                "cta_url": "https://sturgeon.ai/case-studies/techdefense"
            },
            {
                "day": 8,
                "subject": "⚡ Last chance: 14-day free trial expires soon",
                "preview_text": "Unlock AI proposal generation risk-free",
                "body": f"Hi {{{{first_name}}}},\n\n"
                       f"Quick reminder: Your 14-day free trial window is closing.\n\n"
                       f"With Sturgeon AI Pro, you'll unlock:\n\n"
                       f"🎯 AI Proposal Generator - Complete drafts in 90 minutes\n"
                       f"📊 Win Probability Scoring - Know which opps to pursue\n"
                       f"🔍 Competitive Intelligence - Track competitors' wins\n"
                       f"⚡ Priority Support - Get help within 2 hours\n\n"
                       f"No credit card required. No risk. Cancel anytime.\n\n"
                       f"[Activate Your Free Trial]\n\n"
                       f"Still have questions? Book a 15-min call: [Schedule Demo]\n\n"
                       f"Best regards,\n"
                       f"Sarah Chen\n"
                       f"Customer Success, Sturgeon AI",
                "cta": "Activate Your Free Trial",
                "cta_url": "https://sturgeon.ai/upgrade?trial=14"
            },
            {
                "day": 12,
                "subject": "💰 Special offer: Get 2 months free (ends Friday)",
                "preview_text": "Save $398 when you upgrade this week",
                "body": f"Hi {{{{first_name}}}},\n\n"
                       f"I wanted to make this a no-brainer for you.\n\n"
                       f"Upgrade to Sturgeon AI Pro this week and get:\n\n"
                       f"✅ 2 months FREE ($398 value)\n"
                       f"✅ Personalized onboarding session\n"
                       f"✅ Priority implementation support\n\n"
                       f"That's 14 months for the price of 12.\n\n"
                       f"But this offer expires Friday at midnight.\n\n"
                       f"Here's what you'll unlock immediately:\n"
                       f"• AI Proposal Generator\n"
                       f"• Unlimited opportunity tracking\n"
                       f"• Advanced analytics and reporting\n"
                       f"• Priority support (2-hour response)\n\n"
                       f"Ready to 10x your BD efficiency? [Claim Your Offer]\n\n"
                       f"P.S. Have questions? Reply to this email or [book a quick call].\n\n"
                       f"Best,\n"
                       f"Sarah",
                "cta": "Claim Your Offer",
                "cta_url": "https://sturgeon.ai/upgrade?promo=2MONTHSFREE"
            },
            {
                "day": 16,
                "subject": "{{first_name}}, what's holding you back?",
                "preview_text": "Let's address your concerns about upgrading",
                "body": f"Hi {{{{first_name}}}},\n\n"
                       f"I noticed you haven't upgraded yet, and I wanted to check in.\n\n"
                       f"Is there something holding you back? Common concerns we hear:\n\n"
                       f"❓ \"Is it worth the investment?\"\n"
                       f"→ Average customer wins 1 additional contract worth $500K+ in first 6 months\n\n"
                       f"❓ \"Will it work for my company size?\"\n"
                       f"→ We work with contractors from 5 to 5,000 employees\n\n"
                       f"❓ \"How long does implementation take?\"\n"
                       f"→ Most customers are fully set up in under 2 hours\n\n"
                       f"❓ \"What if I need help?\"\n"
                       f"→ Pro customers get priority support with 2-hour response time\n\n"
                       f"Want to discuss your specific situation? [Book a 15-min call] - no pressure, just answers.\n\n"
                       f"Or start your risk-free trial: [Try Pro Free for 14 Days]\n\n"
                       f"Best,\n"
                       f"Sarah Chen\n"
                       f"Customer Success, Sturgeon AI",
                "cta": "Book a 15-min Call",
                "cta_url": "https://sturgeon.ai/book-demo"
            },
            {
                "day": 21,
                "subject": "Final note: We'd love your feedback",
                "preview_text": "Help us improve Sturgeon AI",
                "body": f"Hi {{{{first_name}}}},\n\n"
                       f"I'll keep this brief.\n\n"
                       f"It seems like Sturgeon AI Pro isn't the right fit for you right now, and that's okay.\n\n"
                       f"But I'd love to understand why so we can improve.\n\n"
                       f"Would you mind answering one quick question?\n\n"
                       f"What would make you consider upgrading?\n"
                       f"[ ] Lower price\n"
                       f"[ ] More features\n"
                       f"[ ] Better onboarding\n"
                       f"[ ] Not the right time\n"
                       f"[ ] Other: ___________\n\n"
                       f"[Submit Feedback] (takes 30 seconds)\n\n"
                       f"Your input helps us build a better product for contractors like you.\n\n"
                       f"And hey - you're always welcome to upgrade whenever you're ready. The offer stands.\n\n"
                       f"Thanks for trying Sturgeon AI.\n\n"
                       f"Best regards,\n"
                       f"Sarah Chen\n"
                       f"Customer Success, Sturgeon AI\n\n"
                       f"P.S. You'll stay on our free plan with access to basic features. We're not going anywhere!",
                "cta": "Submit Feedback",
                "cta_url": "https://sturgeon.ai/feedback"
            }
        ]
        
        sequence = {
            "campaign_name": f"Email Nurture - {segment_data['name']} - {goal.replace('_', ' ').title()}",
            "segment": segment,
            "goal": goal,
            "sequence_type": "Conversion Nurture",
            "total_emails": len(emails),
            "timeline_days": 21,
            "sequence": emails,
            "success_metrics": {
                "email_open_rate": 0.42,
                "click_through_rate": 0.18,
                "trial_start_rate": 0.15,
                "trial_to_paid_conversion": 0.35,
                "overall_conversion": 0.052
            },
            "a_b_test_variables": [
                "Subject line urgency vs. curiosity",
                "CTA button color (blue vs. green)",
                "Email length (short vs. detailed)",
                "Social proof placement (top vs. bottom)",
                "Sender name (person vs. company)"
            ],
            "segmentation_rules": {
                "engaged": "Opened 3+ emails or clicked any CTA",
                "hot": "Clicked trial CTA but didn't convert",
                "cold": "No opens after email 3"
            }
        }
        
        return sequence


# Create singleton instance
campaign_gen = CampaignGenerator()
