"""
Marketing Director Agent - Core Intelligence System

This module provides the core AI-powered marketing director agent with strategic
planning, campaign oversight, and intelligent decision-making capabilities.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class MarketingDirectorAgent:
    """
    AI-powered Marketing Director Agent with strategic intelligence.
    
    Provides high-level marketing strategy, campaign oversight, and intelligent
    recommendations for marketing initiatives.
    """
    
    SYSTEM_PROMPT = """You are an expert Marketing Director AI with deep expertise in:
    
    - Strategic marketing planning and execution
    - Multi-channel campaign development (digital, social, content, email, events)
    - Brand positioning and messaging strategy
    - Target audience analysis and segmentation
    - Marketing budget optimization and ROI analysis
    - Performance metrics and KPI tracking
    - Competitive analysis and market research
    - Growth marketing and customer acquisition
    - Marketing technology stack optimization
    
    Your role is to provide strategic guidance, generate comprehensive marketing campaigns,
    optimize budgets for maximum ROI, and deliver data-driven recommendations.
    
    You communicate clearly, back recommendations with reasoning, and always consider
    business objectives, target audience needs, and budget constraints.
    """
    
    def __init__(self, company_context: Optional[Dict[str, Any]] = None):
        """
        Initialize the Marketing Director Agent.
        
        Args:
            company_context: Optional company information including industry, 
                           target market, budget, etc.
        """
        self.company_context = company_context or {}
        self.conversation_history = []
        self.strategies = []
        
    def analyze_market_position(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze company's current market position and competitive landscape.
        
        Args:
            company_info: Dictionary with company details (industry, size, products, etc.)
            
        Returns:
            Dictionary with market analysis and strategic recommendations
        """
        industry = company_info.get('industry', 'General')
        target_market = company_info.get('target_market', 'B2B')
        company_size = company_info.get('size', 'medium')
        
        analysis = {
            'market_position': self._assess_market_position(company_info),
            'opportunities': self._identify_opportunities(industry, target_market),
            'challenges': self._identify_challenges(company_size, industry),
            'competitive_advantages': self._assess_competitive_advantages(company_info),
            'recommended_strategies': self._generate_strategy_recommendations(company_info),
            'timestamp': datetime.now().isoformat()
        }
        
        return analysis
    
    def generate_marketing_strategy(self, 
                                   objectives: List[str],
                                   budget: float,
                                   timeframe: str = "quarterly") -> Dict[str, Any]:
        """
        Generate comprehensive marketing strategy based on objectives and constraints.
        
        Args:
            objectives: List of marketing objectives (e.g., "increase brand awareness")
            budget: Total marketing budget available
            timeframe: Strategy timeframe (quarterly, annual, etc.)
            
        Returns:
            Comprehensive marketing strategy with channel mix and tactics
        """
        strategy = {
            'objectives': objectives,
            'budget': budget,
            'timeframe': timeframe,
            'channel_mix': self._determine_channel_mix(objectives, budget),
            'tactics': self._generate_tactics(objectives, timeframe),
            'kpis': self._define_kpis(objectives),
            'timeline': self._create_timeline(timeframe),
            'success_metrics': self._define_success_metrics(objectives),
            'created_at': datetime.now().isoformat()
        }
        
        self.strategies.append(strategy)
        return strategy
    
    def provide_recommendation(self, 
                              situation: str,
                              context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Provide strategic marketing recommendation for a specific situation.
        
        Args:
            situation: Description of the marketing situation or challenge
            context: Additional context information
            
        Returns:
            Strategic recommendation with reasoning and action steps
        """
        recommendation = {
            'situation': situation,
            'analysis': self._analyze_situation(situation, context or {}),
            'recommendation': self._formulate_recommendation(situation, context or {}),
            'reasoning': self._explain_reasoning(situation, context or {}),
            'action_steps': self._generate_action_steps(situation),
            'expected_outcomes': self._predict_outcomes(situation, context or {}),
            'risks': self._identify_risks(situation),
            'timestamp': datetime.now().isoformat()
        }
        
        return recommendation
    
    def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Interactive chat interface with the marketing director agent.
        
        Args:
            message: User's message or question
            context: Optional context for the conversation
            
        Returns:
            Agent's response
        """
        self.conversation_history.append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        response = self._generate_response(message, context or {})
        
        self.conversation_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    # Private helper methods
    
    def _assess_market_position(self, company_info: Dict[str, Any]) -> str:
        """Assess the company's current market position."""
        size = company_info.get('size', 'medium')
        market_share = company_info.get('market_share', 'emerging')
        
        positions = {
            'emerging': 'Emerging player with growth potential',
            'established': 'Established presence with loyal customer base',
            'leader': 'Market leader with strong brand recognition'
        }
        
        return positions.get(market_share, 'Growing market presence')
    
    def _identify_opportunities(self, industry: str, target_market: str) -> List[str]:
        """Identify market opportunities based on industry and target market."""
        opportunities = [
            f"Digital transformation in {industry} sector",
            f"Growing {target_market} market segment",
            "Content marketing and thought leadership",
            "Marketing automation and personalization",
            "Strategic partnerships and co-marketing"
        ]
        return opportunities[:3]
    
    def _identify_challenges(self, size: str, industry: str) -> List[str]:
        """Identify potential challenges."""
        challenges = {
            'small': ["Limited budget allocation", "Building brand awareness", "Competing with larger players"],
            'medium': ["Scaling marketing operations", "Maintaining growth momentum", "Market differentiation"],
            'large': ["Market saturation", "Maintaining innovation", "Global market expansion"]
        }
        return challenges.get(size, challenges['medium'])
    
    def _assess_competitive_advantages(self, company_info: Dict[str, Any]) -> List[str]:
        """Assess competitive advantages."""
        advantages = [
            "Innovative product offerings",
            "Strong customer relationships",
            "Agile marketing approach"
        ]
        
        if company_info.get('unique_value_prop'):
            advantages.insert(0, company_info['unique_value_prop'])
        
        return advantages[:3]
    
    def _generate_strategy_recommendations(self, company_info: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations."""
        return [
            "Develop integrated multi-channel marketing approach",
            "Invest in content marketing and SEO",
            "Leverage marketing automation for lead nurturing",
            "Build strategic partnerships for market expansion",
            "Implement data-driven decision making"
        ][:3]
    
    def _determine_channel_mix(self, objectives: List[str], budget: float) -> Dict[str, float]:
        """Determine optimal channel budget allocation."""
        # Base allocation
        channel_mix = {
            'digital_advertising': 0.30,
            'content_marketing': 0.25,
            'social_media': 0.20,
            'email_marketing': 0.10,
            'events': 0.10,
            'other': 0.05
        }
        
        # Adjust based on objectives
        if any('brand awareness' in obj.lower() for obj in objectives):
            channel_mix['social_media'] += 0.05
            channel_mix['content_marketing'] += 0.05
            channel_mix['other'] -= 0.10
        
        # Calculate actual budget amounts
        return {channel: budget * allocation for channel, allocation in channel_mix.items()}
    
    def _generate_tactics(self, objectives: List[str], timeframe: str) -> List[Dict[str, Any]]:
        """Generate specific marketing tactics."""
        tactics = [
            {
                'name': 'Content Marketing Campaign',
                'description': 'Create thought leadership content series',
                'channels': ['blog', 'linkedin', 'email'],
                'duration': timeframe
            },
            {
                'name': 'Digital Advertising Push',
                'description': 'Targeted digital ad campaigns',
                'channels': ['google_ads', 'linkedin_ads', 'facebook_ads'],
                'duration': timeframe
            },
            {
                'name': 'Email Nurture Campaign',
                'description': 'Automated lead nurturing sequences',
                'channels': ['email'],
                'duration': timeframe
            }
        ]
        return tactics
    
    def _define_kpis(self, objectives: List[str]) -> List[Dict[str, Any]]:
        """Define Key Performance Indicators."""
        kpi_map = {
            'awareness': ['Website Traffic', 'Social Media Reach', 'Brand Mentions'],
            'leads': ['Lead Generation', 'Conversion Rate', 'Cost per Lead'],
            'revenue': ['Revenue Growth', 'Customer Acquisition Cost', 'Customer Lifetime Value'],
            'engagement': ['Engagement Rate', 'Email Open Rate', 'Time on Site']
        }
        
        kpis = []
        for objective in objectives:
            obj_lower = objective.lower()
            for key, metrics in kpi_map.items():
                if key in obj_lower:
                    kpis.extend([{'metric': m, 'target': 'TBD'} for m in metrics])
        
        # Default KPIs if none matched
        if not kpis:
            kpis = [
                {'metric': 'Lead Generation', 'target': 'Increase by 25%'},
                {'metric': 'Website Traffic', 'target': 'Increase by 30%'},
                {'metric': 'Conversion Rate', 'target': 'Improve by 15%'}
            ]
        
        return kpis[:5]
    
    def _create_timeline(self, timeframe: str) -> List[Dict[str, str]]:
        """Create implementation timeline."""
        if timeframe == 'quarterly':
            return [
                {'phase': 'Month 1', 'focus': 'Strategy & Setup'},
                {'phase': 'Month 2', 'focus': 'Execution & Launch'},
                {'phase': 'Month 3', 'focus': 'Optimization & Analysis'}
            ]
        else:
            return [
                {'phase': 'Q1', 'focus': 'Foundation & Launch'},
                {'phase': 'Q2', 'focus': 'Scale & Optimize'},
                {'phase': 'Q3', 'focus': 'Expand & Innovate'},
                {'phase': 'Q4', 'focus': 'Analyze & Plan'}
            ]
    
    def _define_success_metrics(self, objectives: List[str]) -> Dict[str, str]:
        """Define what success looks like."""
        return {
            'primary': 'Achievement of stated objectives within budget',
            'secondary': 'Positive ROI and improved marketing efficiency',
            'long_term': 'Sustainable growth and market position improvement'
        }
    
    def _analyze_situation(self, situation: str, context: Dict[str, Any]) -> str:
        """Analyze a marketing situation."""
        return f"Analysis: The situation presents an opportunity to leverage strategic marketing initiatives. Consider the current market conditions and available resources."
    
    def _formulate_recommendation(self, situation: str, context: Dict[str, Any]) -> str:
        """Formulate a strategic recommendation."""
        return "Recommended approach: Implement a data-driven, multi-channel strategy focused on measurable outcomes and iterative optimization."
    
    def _explain_reasoning(self, situation: str, context: Dict[str, Any]) -> str:
        """Explain the reasoning behind recommendation."""
        return "This approach balances risk with opportunity, leverages existing strengths, and positions for scalable growth."
    
    def _generate_action_steps(self, situation: str) -> List[str]:
        """Generate specific action steps."""
        return [
            "Conduct detailed situation analysis",
            "Define clear success metrics",
            "Develop implementation plan",
            "Execute with monitoring",
            "Analyze and optimize"
        ]
    
    def _predict_outcomes(self, situation: str, context: Dict[str, Any]) -> List[str]:
        """Predict expected outcomes."""
        return [
            "Improved marketing performance",
            "Better resource allocation",
            "Increased ROI",
            "Enhanced market position"
        ]
    
    def _identify_risks(self, situation: str) -> List[str]:
        """Identify potential risks."""
        return [
            "Market volatility",
            "Budget constraints",
            "Execution challenges",
            "Competitive response"
        ]
    
    def _generate_response(self, message: str, context: Dict[str, Any]) -> str:
        """Generate response to user message."""
        message_lower = message.lower()
        
        if 'budget' in message_lower or 'cost' in message_lower:
            return self._budget_response(message, context)
        elif 'campaign' in message_lower:
            return self._campaign_response(message, context)
        elif 'roi' in message_lower or 'return' in message_lower:
            return self._roi_response(message, context)
        elif 'strategy' in message_lower:
            return self._strategy_response(message, context)
        else:
            return self._general_response(message, context)
    
    def _budget_response(self, message: str, context: Dict[str, Any]) -> str:
        """Generate budget-related response."""
        return ("For budget optimization, I recommend a balanced approach across channels. "
                "Typically, allocate 30% to digital advertising, 25% to content marketing, "
                "20% to social media, and reserve 25% for testing and optimization. "
                "Would you like me to create a detailed budget allocation plan?")
    
    def _campaign_response(self, message: str, context: Dict[str, Any]) -> str:
        """Generate campaign-related response."""
        return ("I can help you design a comprehensive marketing campaign. "
                "A successful campaign typically includes: clear objectives, target audience definition, "
                "multi-channel approach, compelling creative, and measurement plan. "
                "What are your primary campaign objectives?")
    
    def _roi_response(self, message: str, context: Dict[str, Any]) -> str:
        """Generate ROI-related response."""
        return ("ROI optimization is crucial. I recommend tracking metrics like Customer Acquisition Cost (CAC), "
                "Customer Lifetime Value (CLV), and channel-specific ROI. "
                "Aim for a 3:1 return ratio minimum, with top performers achieving 5:1 or better. "
                "Would you like me to analyze your current ROI and suggest improvements?")
    
    def _strategy_response(self, message: str, context: Dict[str, Any]) -> str:
        """Generate strategy-related response."""
        return ("Strategic marketing planning should align with business objectives. "
                "I recommend a quarterly planning cycle with monthly reviews. "
                "Key elements include market analysis, competitive positioning, channel strategy, "
                "and performance tracking. Would you like me to develop a strategy for your specific situation?")
    
    def _general_response(self, message: str, context: Dict[str, Any]) -> str:
        """Generate general response."""
        return ("As your Marketing Director AI, I'm here to help with strategic planning, "
                "campaign development, budget optimization, and ROI analysis. "
                "I can analyze your market position, recommend strategies, and help execute campaigns. "
                "What specific marketing challenge can I help you with today?")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def get_strategies(self) -> List[Dict[str, Any]]:
        """Get all generated strategies."""
        return self.strategies
    
    def export_strategy(self, strategy_index: int = -1) -> str:
        """Export strategy as JSON string."""
        if not self.strategies:
            return json.dumps({'error': 'No strategies available'})
        
        strategy = self.strategies[strategy_index]
        return json.dumps(strategy, indent=2)
