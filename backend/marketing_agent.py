"""
STURGEON AI MARKETING DIRECTOR AGENT
INTERNAL USE ONLY - TRAPIER MANAGEMENT LLC

This is a private AI agent designed exclusively for Harold Trapier and Trapier Management LLC
to develop and execute marketing strategies for Sturgeon AI.

AGENT IDENTITY:
- Role: Chief Marketing Officer for Sturgeon AI
- Reporting to: Harold Trapier, Founder
- Purpose: Drive customer acquisition, brand positioning, and revenue growth
- Constraint: Internal tool only - NOT customer-facing

CORE COMPETENCIES:
1. Government Contracting Market Intelligence
2. B2B SaaS Marketing Strategy
3. Defense Industry Positioning
4. Lead Generation & Conversion Optimization
5. Content Marketing & Thought Leadership
6. LinkedIn Outreach Campaign Design
7. ROI-Driven Marketing Analytics
"""

AGENT_SYSTEM_PROMPT = """You are the Marketing Director for Sturgeon AI, an AI-powered government contracting intelligence platform built by Trapier Management LLC, a Service-Connected Disabled Veteran-Owned Small Business (SDVOSB).

YOUR MISSION:
Drive qualified lead acquisition and revenue growth for Sturgeon AI by executing data-driven marketing campaigns targeting government contractors, defense industry professionals, and procurement specialists.

PRODUCT KNOWLEDGE - STURGEON AI:
- AI-powered government contracting intelligence platform
- Analyzes SAM.gov opportunities, contract histories, competitor tracking
- Target users: GovCon professionals, proposal teams, BD directors, small businesses
- Value proposition: Win more federal contracts through AI-powered intelligence
- Pricing: Freemium model with premium tiers ($99-$499/month)
- Competitive advantage: SDVOSB status, AI-native platform, real-time insights

TARGET MARKET:
Primary:
- Defense contractors (small to mid-size)
- Government consulting firms
- IT services companies pursuing federal contracts
- Engineering firms in defense sector

Secondary:
- Construction companies (federal projects)
- Professional services firms
- Management consultancies

MARKETING CONSTRAINTS:
1. Budget: Bootstrap/lean marketing approach
2. Timeline: Aggressive growth targets (0 to 1000 users in 6 months)
3. Resources: Solo founder with AI automation
4. Channel focus: LinkedIn, email, content marketing
5. Compliance: Federal procurement advertising regulations

YOUR CAPABILITIES:
1. Campaign Strategy Development
   - Multi-channel marketing campaigns
   - A/B testing frameworks
   - Conversion funnel optimization
   - Budget allocation strategies

2. Content Creation
   - LinkedIn posts and articles
   - Email sequences
   - Case studies and white papers
   - Video script outlines
   - Blog content calendars

3. Lead Generation
   - LinkedIn outreach scripts
   - Lead magnet development
   - Landing page optimization
   - Lead scoring frameworks

4. Analytics & Optimization
   - Campaign performance analysis
   - Conversion rate optimization
   - Customer acquisition cost (CAC) calculations
   - Lifetime value (LTV) projections

5. Competitive Intelligence
   - Competitor analysis
   - Market positioning
   - Pricing strategy
   - Feature differentiation

6. Sales Enablement
   - Sales scripts and talking points
   - Demo flows
   - Objection handling guides
   - Proposal templates

OPERATING PRINCIPLES:
1. EXECUTION SPEED: Military precision, immediate action
2. ROI OBSESSION: Every campaign must show measurable results
3. DATA-DRIVEN: Metrics over opinions, testing over guessing
4. LEAN APPROACH: Maximum impact with minimum spend
5. VETERAN FOCUS: Leverage SDVOSB status authentically
6. NO BUZZWORDS: Clear, direct communication like Harold expects

DELIVERABLE FORMATS:
- Campaign briefs: 1-page actionable plans
- Content: Ready-to-publish, no theory
- Scripts: Word-for-word copy, not frameworks
- Analytics: Numbers and next actions, not analysis paralysis
- Strategy: 3-5 specific tactics, not philosophical discussions

HAROLD'S PREFERENCES (CRITICAL):
- Wants comprehensive solutions ("all" components)
- Zero tolerance for buzzwords or theory
- Execution-focused, not discussion-focused
- Measurable outcomes required
- Direct military-style communication
- Impatient with incremental approaches

When Harold asks for marketing support, you provide:
1. Complete campaign ready to launch
2. All assets created (copy, scripts, sequences)
3. Specific metrics to track
4. Timeline for execution
5. Expected ROI projections

You do NOT provide:
- Theoretical frameworks without execution plans
- "Here are some ideas to consider"
- Requests for more information before acting
- Academic marketing concepts
- Fluffy brand messaging without conversion focus

REMEMBER: You are an internal tool for Trapier Management to market Sturgeon AI effectively. You serve Harold's mission to build a dominant government contracting intelligence platform. Every recommendation must drive toward measurable business outcomes.
"""

# Marketing campaign templates
CAMPAIGN_TEMPLATES = {
    "linkedin_outreach": {
        "objective": "Connect with government contracting professionals",
        "sequence_length": 5,
        "cadence_days": [0, 3, 7, 14, 21],
        "kpis": ["connection_rate", "response_rate", "demo_booking_rate"]
    },
    
    "email_nurture": {
        "objective": "Convert free users to paid subscribers",
        "sequence_length": 7,
        "cadence_days": [0, 2, 5, 9, 14, 21, 28],
        "kpis": ["open_rate", "click_rate", "conversion_rate"]
    },
    
    "content_marketing": {
        "objective": "Establish thought leadership and drive organic traffic",
        "frequency": "3x per week",
        "channels": ["LinkedIn", "Blog", "Newsletter"],
        "kpis": ["engagement_rate", "traffic", "lead_generation"]
    },
    
    "paid_acquisition": {
        "objective": "Acquire qualified leads at <$50 CAC",
        "channels": ["LinkedIn Ads", "Google Ads"],
        "budget_range": "$2000-5000/month",
        "kpis": ["cpc", "conversion_rate", "cac", "roas"]
    }
}

# Target audience personas
PERSONAS = {
    "bd_director": {
        "title": "Business Development Director",
        "company_size": "50-500 employees",
        "pain_points": [
            "Missing contract opportunities",
            "Inefficient competitive intelligence",
            "Manual SAM.gov monitoring",
            "Limited market visibility"
        ],
        "goals": [
            "Increase win rate",
            "Reduce bid preparation time",
            "Expand contract pipeline",
            "Beat competitors to opportunities"
        ],
        "objections": [
            "Already using GovWin/Deltek",
            "Too expensive",
            "Learning curve concerns",
            "Integration challenges"
        ]
    },
    
    "small_biz_owner": {
        "title": "Small Business Owner / Founder",
        "company_size": "1-50 employees",
        "pain_points": [
            "Overwhelmed by complexity",
            "Limited BD resources",
            "Can't compete with large contractors",
            "Don't know where to start"
        ],
        "goals": [
            "Win first federal contract",
            "Qualify for set-asides",
            "Grow federal revenue",
            "Compete effectively"
        ],
        "objections": [
            "Too sophisticated for our needs",
            "Can't afford subscription",
            "Need training/support",
            "Prefer doing it manually"
        ]
    },
    
    "proposal_manager": {
        "title": "Proposal Manager / Capture Manager",
        "company_size": "100-1000 employees",
        "pain_points": [
            "Tight proposal deadlines",
            "Need competitive intelligence fast",
            "Inconsistent win rate",
            "Manual research bottlenecks"
        ],
        "goals": [
            "Faster proposal development",
            "Better win probability",
            "Comprehensive competitor analysis",
            "Data-driven pricing"
        ],
        "objections": [
            "Security clearance concerns",
            "Already have internal tools",
            "Need IT approval",
            "Procurement process delays"
        ]
    }
}

# Channel-specific best practices
CHANNEL_STRATEGIES = {
    "linkedin": {
        "posting_frequency": "5x per week",
        "best_times": ["Tuesday 8am EST", "Wednesday 9am EST", "Thursday 10am EST"],
        "content_mix": {
            "thought_leadership": 40,
            "product_updates": 20,
            "customer_success": 20,
            "industry_insights": 20
        },
        "engagement_tactics": [
            "Comment on industry leader posts",
            "Share relevant industry news with perspective",
            "Engage in GovCon groups",
            "Host LinkedIn Live sessions"
        ]
    },
    
    "email": {
        "optimal_send_times": ["Tuesday 10am EST", "Thursday 2pm EST"],
        "subject_line_length": "40-50 characters",
        "body_length": "100-200 words",
        "cta_placement": "Above the fold",
        "personalization_tokens": ["first_name", "company", "recent_bid", "contract_type"]
    },
    
    "content": {
        "blog_frequency": "2x per week",
        "optimal_length": "1200-1500 words",
        "seo_keywords": [
            "government contracting software",
            "SAM.gov automation",
            "federal contract intelligence",
            "GovCon AI tools",
            "proposal automation"
        ],
        "content_types": [
            "How-to guides",
            "Case studies",
            "Industry analysis",
            "Tool comparisons",
            "Regulatory updates"
        ]
    }
}

# Key metrics and targets
MARKETING_METRICS = {
    "acquisition": {
        "monthly_new_users": 200,  # count
        "cac_target": 50,  # USD
        "payback_period_months": 6,  # months
        "free_to_paid_conversion": 5  # percent
    },
    
    "engagement": {
        "dau_mau_ratio": 0.3,  # ratio (0-1)
        "weekly_active_users": 150,  # count
        "feature_adoption_rate": 60,  # percent
        "nps_score": 50  # score (-100 to 100)
    },
    
    "revenue": {
        "mrr_target": 10000,  # USD per month
        "arr_target": 120000,  # USD per year
        "ltv_target": 3000,  # USD
        "churn_rate_max": 5  # percent
    }
}


class MarketingDirectorAgent:
    """
    Marketing Director AI Agent for Sturgeon AI
    
    This agent provides comprehensive marketing strategy, campaign execution,
    and analytics support for Trapier Management LLC's Sturgeon AI platform.
    """
    
    def __init__(self):
        self.system_prompt = AGENT_SYSTEM_PROMPT
        self.campaign_templates = CAMPAIGN_TEMPLATES
        self.personas = PERSONAS
        self.channel_strategies = CHANNEL_STRATEGIES
        self.marketing_metrics = MARKETING_METRICS
    
    def get_campaign_template(self, campaign_type: str) -> dict:
        """
        Retrieve a specific campaign template
        
        Args:
            campaign_type: One of 'linkedin_outreach', 'email_nurture', 
                          'content_marketing', 'paid_acquisition'
        
        Returns:
            Campaign template dictionary
        """
        return self.campaign_templates.get(campaign_type, {})
    
    def get_persona(self, persona_type: str) -> dict:
        """
        Retrieve a target audience persona
        
        Args:
            persona_type: One of 'bd_director', 'small_biz_owner', 'proposal_manager'
        
        Returns:
            Persona dictionary with pain points, goals, and objections
        """
        return self.personas.get(persona_type, {})
    
    def get_channel_strategy(self, channel: str) -> dict:
        """
        Retrieve channel-specific marketing strategy
        
        Args:
            channel: One of 'linkedin', 'email', 'content'
        
        Returns:
            Channel strategy dictionary
        """
        return self.channel_strategies.get(channel, {})
    
    def get_metrics(self, metric_category: str = None) -> dict:
        """
        Retrieve marketing metrics and targets
        
        Args:
            metric_category: Optional category ('acquisition', 'engagement', 'revenue')
                           If None, returns all metrics
        
        Returns:
            Metrics dictionary
        """
        if metric_category:
            return self.marketing_metrics.get(metric_category, {})
        return self.marketing_metrics
    
    def generate_campaign_brief(self, campaign_type: str, persona_type: str) -> dict:
        """
        Generate a complete campaign brief combining template, persona, and strategy
        
        Args:
            campaign_type: Campaign template to use
            persona_type: Target persona
        
        Returns:
            Complete campaign brief ready for execution
        """
        campaign = self.get_campaign_template(campaign_type)
        persona = self.get_persona(persona_type)
        
        # Determine primary channel based on campaign type
        primary_channel = "linkedin" if "linkedin" in campaign_type else "email"
        if campaign_type == "content_marketing":
            primary_channel = "content"
        
        channel = self.get_channel_strategy(primary_channel)
        
        return {
            "campaign": campaign,
            "target_persona": persona,
            "channel_strategy": channel,
            "execution_ready": True,
            "created_for": "Trapier Management LLC - Internal Use Only"
        }
    
    def get_all_campaigns(self) -> list:
        """Get list of all available campaign types"""
        return list(self.campaign_templates.keys())
    
    def get_all_personas(self) -> list:
        """Get list of all available persona types"""
        return list(self.personas.keys())
    
    def get_all_channels(self) -> list:
        """Get list of all available channel strategies"""
        return list(self.channel_strategies.keys())


# Singleton instance for easy access
marketing_director = MarketingDirectorAgent()
