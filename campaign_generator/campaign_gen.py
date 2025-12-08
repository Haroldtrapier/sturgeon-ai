"""
Campaign Generation Module
Generates LinkedIn outreach campaigns with personalized messaging sequences
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone


# Persona definitions with LinkedIn targeting criteria
PERSONA_DEFINITIONS = {
    "bd_director": {
        "title": "Business Development Director",
        "job_titles": [
            "Business Development Director",
            "VP of Business Development",
            "Director of BD",
            "Head of Business Development",
            "Senior BD Manager"
        ],
        "industries": [
            "Government Contracting",
            "Defense",
            "Federal Consulting",
            "Technology Services",
            "Professional Services"
        ],
        "seniority_levels": ["Director", "VP", "Head"],
        "company_sizes": ["51-200", "201-500", "501-1000", "1001-5000"],
        "locations": ["United States", "Washington DC Metro Area"],
        "interests": [
            "Government Contracts",
            "Federal Procurement",
            "GSA Schedules",
            "SAM Registration",
            "RFP Response"
        ]
    },
    "procurement_officer": {
        "title": "Procurement Officer",
        "job_titles": [
            "Procurement Officer",
            "Contracting Officer",
            "Purchasing Manager",
            "Procurement Specialist",
            "Contract Administrator"
        ],
        "industries": [
            "Government",
            "Federal Government",
            "Public Sector",
            "Defense",
            "Federal Agencies"
        ],
        "seniority_levels": ["Manager", "Specialist", "Officer"],
        "company_sizes": ["201-500", "501-1000", "1001-5000", "5001+"],
        "locations": ["United States", "Washington DC Metro Area"],
        "interests": [
            "Federal Acquisition",
            "Procurement Management",
            "Contract Negotiation",
            "FAR Compliance"
        ]
    },
    "grant_manager": {
        "title": "Grant Manager",
        "job_titles": [
            "Grant Manager",
            "Grant Administrator",
            "Grants Director",
            "Grant Writer",
            "Development Director"
        ],
        "industries": [
            "Nonprofit",
            "Education",
            "Healthcare",
            "Research",
            "Social Services"
        ],
        "seniority_levels": ["Manager", "Director", "Administrator"],
        "company_sizes": ["11-50", "51-200", "201-500"],
        "locations": ["United States"],
        "interests": [
            "Grant Writing",
            "Federal Grants",
            "Grant Management",
            "Nonprofit Funding",
            "Grant Compliance"
        ]
    }
}


# Message templates for 5-message sequence
MESSAGE_TEMPLATES = {
    "bd_director": {
        "message_1": {
            "subject": "Streamline Your Government Contract Pipeline",
            "body": "Hi {first_name},\n\nI noticed you're leading business development at {company}. As someone focused on government contracting, you know how time-consuming it can be to track opportunities across SAM.gov, Grants.gov, and agency-specific portals.\n\nSturgeon AI helps BD teams like yours automate contract discovery and match analysis, saving 15+ hours per week. Would you be open to a quick chat about how we're helping companies like {similar_company} win more federal contracts?\n\nBest,\n{sender_name}"
        },
        "message_2": {
            "subject": "Quick question about your BD process",
            "body": "Hi {first_name},\n\nFollowing up on my previous message. I wanted to share a specific example:\n\nOne of our BD director clients was spending 20 hours/week manually searching for RFPs. After implementing Sturgeon AI, they:\n- Reduced search time by 80%\n- Increased qualified opportunities by 45%\n- Improved win rate by 23%\n\nWould a 15-minute demo make sense for {company}?\n\nBest,\n{sender_name}"
        },
        "message_3": {
            "subject": "AI-powered contract intelligence for {company}",
            "body": "Hi {first_name},\n\nI understand you're busy, so I'll keep this brief. \n\nSturgeon AI offers:\n✓ Real-time monitoring of 50,000+ opportunities\n✓ AI-powered match scoring for your capabilities\n✓ Automated RFP analysis and compliance checking\n✓ Competitive intelligence and past performance data\n\nWe've helped 200+ government contractors optimize their BD pipeline. Would next Tuesday or Thursday work for a quick call?\n\nBest,\n{sender_name}"
        },
        "message_4": {
            "subject": "Case study: 3x pipeline growth in 90 days",
            "body": "Hi {first_name},\n\nI wanted to share how Sturgeon AI helped a company similar to {company} achieve remarkable results:\n\n📊 Case Study: Federal IT Contractor\n- 3x increase in qualified pipeline\n- 15 hours/week saved per BD team member\n- 31% improvement in proposal quality scores\n- $12M in new contract wins in Q1\n\nI'd love to explore how we can deliver similar results for {company}. Are you available for a brief call this week?\n\nBest,\n{sender_name}"
        },
        "message_5": {
            "subject": "Last follow-up - exclusive demo offer",
            "body": "Hi {first_name},\n\nThis is my last follow-up. I don't want to be a pest, but I genuinely believe Sturgeon AI could significantly impact {company}'s government contracting success.\n\nI'm offering an exclusive 30-day trial with:\n- Full platform access\n- Personalized onboarding\n- Custom opportunity matching for your capabilities\n- No credit card required\n\nIf you're interested, just reply \"Yes\" and I'll set everything up. Otherwise, I'll assume the timing isn't right and won't reach out again.\n\nBest wishes,\n{sender_name}"
        }
    },
    "procurement_officer": {
        "message_1": {
            "subject": "Streamline your procurement workflows",
            "body": "Hi {first_name},\n\nAs a procurement professional at {company}, you understand the complexity of managing federal acquisition processes. Sturgeon AI helps procurement teams automate vendor discovery and compliance verification.\n\nWould you be interested in learning how we're helping agencies improve their procurement efficiency?\n\nBest,\n{sender_name}"
        },
        "message_2": {
            "subject": "Follow-up: Procurement automation",
            "body": "Hi {first_name},\n\nI wanted to follow up and share that Sturgeon AI helps procurement officers:\n- Automate vendor qualification checks\n- Track compliance requirements\n- Streamline RFP management\n\nWould a brief demo be helpful?\n\nBest,\n{sender_name}"
        },
        "message_3": {
            "subject": "AI for procurement teams",
            "body": "Hi {first_name},\n\nQuick update - our platform now includes:\n✓ Automated FAR compliance checking\n✓ Vendor performance analytics\n✓ Real-time market intelligence\n\nInterested in a 15-minute overview?\n\nBest,\n{sender_name}"
        },
        "message_4": {
            "subject": "Case study for procurement teams",
            "body": "Hi {first_name},\n\nA federal agency recently used Sturgeon AI to reduce their procurement cycle time by 40%. I'd love to share the details with you.\n\nAvailable for a quick call?\n\nBest,\n{sender_name}"
        },
        "message_5": {
            "subject": "Final follow-up",
            "body": "Hi {first_name},\n\nThis will be my last message. If procurement efficiency is a priority, I'm happy to set up a trial. Otherwise, best of luck with your initiatives.\n\nBest,\n{sender_name}"
        }
    },
    "grant_manager": {
        "message_1": {
            "subject": "Maximize your grant success rate",
            "body": "Hi {first_name},\n\nI see you're managing grants at {company}. Finding and tracking federal grant opportunities across multiple portals can be overwhelming.\n\nSturgeon AI helps grant managers automate opportunity discovery and eligibility matching. Would you be open to learning more?\n\nBest,\n{sender_name}"
        },
        "message_2": {
            "subject": "Grant discovery automation",
            "body": "Hi {first_name},\n\nFollowing up - grant managers using Sturgeon AI report:\n- 60% time savings on opportunity research\n- 45% increase in qualified applications\n- Better grant compliance tracking\n\nInterested in a demo?\n\nBest,\n{sender_name}"
        },
        "message_3": {
            "subject": "AI-powered grant intelligence",
            "body": "Hi {first_name},\n\nOur platform helps grant teams:\n✓ Monitor 10,000+ federal grant opportunities\n✓ AI-powered eligibility matching\n✓ Automated deadline tracking\n✓ Compliance requirement analysis\n\nWould next week work for a call?\n\nBest,\n{sender_name}"
        },
        "message_4": {
            "subject": "Grant success story",
            "body": "Hi {first_name},\n\nA nonprofit similar to {company} used Sturgeon AI to increase their grant success rate by 35%. I'd love to share their approach with you.\n\nAvailable for a brief chat?\n\nBest,\n{sender_name}"
        },
        "message_5": {
            "subject": "Last outreach",
            "body": "Hi {first_name},\n\nMy final message - if grant discovery and management is a challenge, I'm offering a free 30-day trial. Just let me know if you're interested.\n\nOtherwise, best of luck with your grant initiatives!\n\nBest,\n{sender_name}"
        }
    }
}


def generate_linkedin_outreach_campaign(
    target_persona: str,
    target_count: int,
    sender_name: Optional[str] = "Alex from Sturgeon AI",
    company_context: Optional[Dict] = None
) -> Dict:
    """
    Generate a LinkedIn outreach campaign with 5-message sequence, targeting, and metrics.
    
    Args:
        target_persona: The persona to target (e.g., "bd_director", "procurement_officer", "grant_manager")
        target_count: Number of targets to reach out to
        sender_name: Name of the sender (default: "Alex from Sturgeon AI")
        company_context: Optional context about the target company
        
    Returns:
        Dictionary containing:
            - messages: List of 5 message templates with subject and body
            - targeting: Targeting criteria for LinkedIn
            - metrics: Expected campaign metrics
            - campaign_summary: Summary of the campaign
            
    Raises:
        ValueError: If target_persona is not recognized or target_count is invalid
    """
    
    # Validate inputs
    if target_persona not in PERSONA_DEFINITIONS:
        available_personas = ", ".join(PERSONA_DEFINITIONS.keys())
        raise ValueError(
            f"Unknown target_persona: '{target_persona}'. "
            f"Available personas: {available_personas}"
        )
    
    if target_count <= 0:
        raise ValueError(f"target_count must be positive, got: {target_count}")
    
    # Get persona and message templates
    persona_def = PERSONA_DEFINITIONS[target_persona]
    message_templates = MESSAGE_TEMPLATES[target_persona]
    
    # Build 5-message sequence
    messages = []
    for i in range(1, 6):
        message_key = f"message_{i}"
        template = message_templates[message_key]
        messages.append({
            "sequence_number": i,
            "subject": template["subject"],
            "body": template["body"],
            "delay_days": (i - 1) * 3,  # Space out messages by 3 days
            "personalization_fields": [
                "{first_name}",
                "{company}",
                "{sender_name}",
                "{similar_company}"
            ]
        })
    
    # Build targeting criteria
    targeting = {
        "persona": target_persona,
        "persona_title": persona_def["title"],
        "job_titles": persona_def["job_titles"],
        "industries": persona_def["industries"],
        "seniority_levels": persona_def["seniority_levels"],
        "company_sizes": persona_def["company_sizes"],
        "locations": persona_def["locations"],
        "interests": persona_def["interests"],
        "estimated_audience_size": _estimate_audience_size(persona_def),
        "target_count": target_count,
        "targeting_precision": "High"
    }
    
    # Calculate expected metrics
    metrics = _calculate_campaign_metrics(target_count)
    
    # Build campaign summary
    campaign_summary = {
        "campaign_type": "LinkedIn Outreach",
        "target_persona": target_persona,
        "target_count": target_count,
        "message_sequence_length": 5,
        "total_campaign_duration_days": 12,  # 5 messages spaced 3 days apart
        "sender": sender_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "ready",
        "estimated_completion_date": _calculate_completion_date(12)
    }
    
    return {
        "messages": messages,
        "targeting": targeting,
        "metrics": metrics,
        "campaign_summary": campaign_summary
    }


def _estimate_audience_size(persona_def: Dict) -> str:
    """Estimate the LinkedIn audience size based on targeting criteria."""
    # Rough estimates based on persona
    base_sizes = {
        "Director": "50,000-100,000",
        "VP": "20,000-50,000",
        "Manager": "100,000-200,000",
        "Officer": "30,000-70,000",
        "Specialist": "80,000-150,000"
    }
    
    # Use first seniority level as proxy
    if persona_def["seniority_levels"]:
        seniority = persona_def["seniority_levels"][0]
        return base_sizes.get(seniority, "50,000-100,000")
    
    return "50,000-100,000"


def _calculate_campaign_metrics(target_count: int) -> Dict:
    """Calculate expected campaign performance metrics."""
    
    # Industry benchmark rates for LinkedIn outreach campaigns
    connection_accept_rate = 0.25  # 25% accept connection requests
    message_open_rate = 0.60  # 60% open messages
    response_rate = 0.08  # 8% respond to messages
    demo_booking_rate = 0.15  # 15% of responders book a demo
    
    # Calculate expected outcomes
    expected_connections = int(target_count * connection_accept_rate)
    expected_opens = int(expected_connections * message_open_rate)
    expected_responses = int(expected_connections * response_rate)
    expected_demos = int(expected_responses * demo_booking_rate)
    
    return {
        "target_count": target_count,
        "expected_connection_accepts": expected_connections,
        "expected_message_opens": expected_opens,
        "expected_responses": expected_responses,
        "expected_demo_bookings": expected_demos,
        "estimated_conversion_rates": {
            "connection_accept_rate": f"{connection_accept_rate * 100:.1f}%",
            "message_open_rate": f"{message_open_rate * 100:.1f}%",
            "response_rate": f"{response_rate * 100:.1f}%",
            "demo_booking_rate": f"{demo_booking_rate * 100:.1f}%"
        },
        "estimated_roi": {
            "cost_per_target": 2.50,  # Estimated cost per LinkedIn outreach
            "total_campaign_cost": target_count * 2.50,
            "cost_per_demo": (target_count * 2.50) / max(expected_demos, 1),
            "expected_pipeline_value": expected_demos * 50000  # $50k average deal size
        }
    }


def _calculate_completion_date(duration_days: int) -> str:
    """Calculate the estimated campaign completion date."""
    from datetime import timedelta
    completion_date = datetime.now(timezone.utc) + timedelta(days=duration_days)
    return completion_date.strftime("%Y-%m-%d")
