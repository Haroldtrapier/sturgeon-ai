"""
ROI Calculator Module

This module provides comprehensive ROI calculation and budget optimization
capabilities for marketing campaigns.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json


class ROICalculator:
    """
    AI-powered ROI calculator for marketing budget optimization.
    
    Provides ROI analysis, budget allocation optimization, and performance predictions.
    """
    
    # Constants
    DEFAULT_ROI_PERCENTAGE = 100
    
    def __init__(self):
        """Initialize the ROI calculator."""
        self.calculations = []
        self.benchmarks = self._load_industry_benchmarks()
    
    @staticmethod
    def _safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
        """Safely perform division, returning default if denominator is zero."""
        return numerator / denominator if denominator != 0 else default
    
    def calculate_campaign_roi(self,
                              campaign_data: Dict[str, Any],
                              results_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate ROI for a completed or ongoing campaign.
        
        Args:
            campaign_data: Campaign budget and cost information
            results_data: Campaign performance and revenue data
            
        Returns:
            Comprehensive ROI analysis with metrics and insights
        """
        total_investment = campaign_data.get('total_budget', 0)
        revenue_generated = results_data.get('revenue', 0)
        
        # Calculate core ROI metrics
        roi_percentage = self._calculate_roi_percentage(revenue_generated, total_investment)
        roas = self._calculate_roas(revenue_generated, total_investment)
        
        # Calculate additional metrics
        leads_generated = results_data.get('leads', 0)
        customers_acquired = results_data.get('customers', 0)
        cost_per_lead = self._safe_divide(total_investment, leads_generated)
        cost_per_acquisition = self._safe_divide(total_investment, customers_acquired)
        
        # Calculate customer lifetime value impact
        avg_customer_value = results_data.get('avg_customer_value', 0)
        ltv_to_cac_ratio = self._safe_divide(avg_customer_value, cost_per_acquisition)
        
        analysis = {
            'campaign_id': campaign_data.get('id', 'unknown'),
            'campaign_name': campaign_data.get('name', 'Campaign'),
            'total_investment': total_investment,
            'revenue_generated': revenue_generated,
            'roi_percentage': round(roi_percentage, 2),
            'roas': round(roas, 2),
            'leads_generated': leads_generated,
            'customers_acquired': customers_acquired,
            'cost_per_lead': round(cost_per_lead, 2),
            'cost_per_acquisition': round(cost_per_acquisition, 2),
            'avg_customer_value': avg_customer_value,
            'ltv_to_cac_ratio': round(ltv_to_cac_ratio, 2),
            'performance_grade': self._grade_performance(roi_percentage, ltv_to_cac_ratio),
            'insights': self._generate_roi_insights(roi_percentage, roas, ltv_to_cac_ratio),
            'recommendations': self._generate_roi_recommendations(campaign_data, roi_percentage),
            'timestamp': datetime.now().isoformat()
        }
        
        self.calculations.append(analysis)
        return analysis
    
    def calculate_channel_roi(self,
                             channel_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate ROI for individual marketing channels.
        
        Args:
            channel_data: Dictionary with channel names as keys and performance data as values
            
        Returns:
            Channel-by-channel ROI analysis with comparisons
        """
        channel_analysis = {}
        
        for channel, data in channel_data.items():
            investment = data.get('spend', 0)
            revenue = data.get('revenue', 0)
            
            channel_analysis[channel] = {
                'investment': investment,
                'revenue': revenue,
                'roi_percentage': self._calculate_roi_percentage(revenue, investment),
                'roas': self._calculate_roas(revenue, investment),
                'cost_per_lead': self._safe_divide(data.get('spend', 0), data.get('leads', 0)),
                'conversion_rate': self._safe_divide(data.get('conversions', 0), data.get('clicks', 0)),
                'performance_tier': self._classify_channel_performance(
                    self._calculate_roi_percentage(revenue, investment)
                )
            }
        
        # Add comparative analysis
        result = {
            'channels': channel_analysis,
            'best_performer': self._identify_best_channel(channel_analysis),
            'worst_performer': self._identify_worst_channel(channel_analysis),
            'optimization_opportunities': self._identify_channel_optimizations(channel_analysis),
            'recommended_shifts': self._recommend_budget_shifts(channel_analysis),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def optimize_budget_allocation(self,
                                  total_budget: float,
                                  channels: List[str],
                                  historical_performance: Optional[Dict[str, Any]] = None,
                                  objectives: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Optimize budget allocation across marketing channels.
        
        Args:
            total_budget: Total marketing budget to allocate
            channels: List of marketing channels
            historical_performance: Past performance data for channels
            objectives: Marketing objectives to optimize for
            
        Returns:
            Optimized budget allocation plan
        """
        # Determine optimal allocation
        if historical_performance:
            allocation = self._allocate_based_on_performance(
                total_budget, channels, historical_performance
            )
        else:
            allocation = self._allocate_based_on_best_practices(
                total_budget, channels, objectives or []
            )
        
        # Calculate expected returns
        expected_returns = self._calculate_expected_returns(allocation, historical_performance)
        
        optimization = {
            'total_budget': total_budget,
            'channels': channels,
            'recommended_allocation': allocation,
            'allocation_percentages': {
                channel: round((amount / total_budget) * 100, 1)
                for channel, amount in allocation.items()
            },
            'expected_returns': expected_returns,
            'expected_roi': round(expected_returns.get('total_roi', 0), 2),
            'confidence_level': self._calculate_confidence_level(historical_performance),
            'rationale': self._explain_allocation_rationale(allocation, historical_performance),
            'optimization_strategy': self._define_optimization_strategy(objectives or []),
            'testing_budget': round(total_budget * 0.15, 2),  # 15% for testing
            'timestamp': datetime.now().isoformat()
        }
        
        return optimization
    
    def predict_campaign_roi(self,
                            campaign_plan: Dict[str, Any],
                            market_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Predict expected ROI for a planned campaign.
        
        Args:
            campaign_plan: Planned campaign details
            market_conditions: Current market condition factors
            
        Returns:
            ROI prediction with confidence intervals
        """
        budget = campaign_plan.get('budget', 0)
        channels = campaign_plan.get('channels', [])
        objective = campaign_plan.get('objective', 'lead_generation')
        
        # Get benchmark performance
        benchmark_roi = self._get_benchmark_roi(objective, channels)
        
        # Adjust for market conditions
        if market_conditions:
            adjustment_factor = self._calculate_market_adjustment(market_conditions)
        else:
            adjustment_factor = 1.0
        
        predicted_roi = benchmark_roi * adjustment_factor
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(predicted_roi)
        
        # Calculate expected outcomes
        expected_revenue = budget * (predicted_roi / 100)
        expected_leads = self._estimate_leads(budget, channels)
        expected_customers = self._estimate_customers(expected_leads, objective)
        
        prediction = {
            'campaign_name': campaign_plan.get('name', 'Campaign'),
            'budget': budget,
            'predicted_roi_percentage': round(predicted_roi, 2),
            'predicted_revenue': round(expected_revenue, 2),
            'predicted_roas': round(expected_revenue / budget, 2) if budget > 0 else 0,
            'expected_leads': int(expected_leads),
            'expected_customers': int(expected_customers),
            'confidence_intervals': confidence_intervals,
            'risk_assessment': self._assess_campaign_risk(campaign_plan),
            'success_probability': self._calculate_success_probability(campaign_plan),
            'key_assumptions': self._list_key_assumptions(campaign_plan),
            'sensitivity_analysis': self._perform_sensitivity_analysis(budget, predicted_roi),
            'timestamp': datetime.now().isoformat()
        }
        
        return prediction
    
    def analyze_budget_efficiency(self,
                                 actual_spend: Dict[str, float],
                                 planned_budget: Dict[str, float],
                                 results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze budget efficiency and spending patterns.
        
        Args:
            actual_spend: Actual spending by channel
            planned_budget: Planned budget by channel
            results: Campaign results and performance
            
        Returns:
            Budget efficiency analysis with recommendations
        """
        efficiency_metrics = {}
        
        for channel in planned_budget.keys():
            planned = planned_budget.get(channel, 0)
            actual = actual_spend.get(channel, 0)
            variance = actual - planned
            variance_percentage = self._safe_divide(variance * 100, planned)
            
            efficiency_metrics[channel] = {
                'planned': planned,
                'actual': actual,
                'variance': round(variance, 2),
                'variance_percentage': round(variance_percentage, 2),
                'efficiency_score': self._calculate_efficiency_score(channel, actual, results),
                'utilization_rate': round((actual / planned * 100), 2) if planned > 0 else 0
            }
        
        analysis = {
            'channel_efficiency': efficiency_metrics,
            'overall_efficiency': self._calculate_overall_efficiency(efficiency_metrics),
            'budget_discipline': self._assess_budget_discipline(actual_spend, planned_budget),
            'spending_patterns': self._analyze_spending_patterns(actual_spend),
            'waste_identification': self._identify_waste(efficiency_metrics, results),
            'efficiency_recommendations': self._generate_efficiency_recommendations(efficiency_metrics),
            'reallocation_suggestions': self._suggest_reallocation(efficiency_metrics, results),
            'timestamp': datetime.now().isoformat()
        }
        
        return analysis
    
    def calculate_customer_acquisition_metrics(self,
                                              campaign_data: Dict[str, Any],
                                              customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive customer acquisition metrics.
        
        Args:
            campaign_data: Campaign spend and details
            customer_data: Customer acquisition and value data
            
        Returns:
            Customer acquisition metrics and analysis
        """
        total_spend = campaign_data.get('total_spend', 0)
        customers_acquired = customer_data.get('customers_acquired', 0)
        
        cac = total_spend / customers_acquired if customers_acquired > 0 else 0
        avg_order_value = customer_data.get('avg_order_value', 0)
        ltv = customer_data.get('customer_ltv', avg_order_value * 3)  # Default 3x AOV
        
        metrics = {
            'customer_acquisition_cost': round(cac, 2),
            'customer_lifetime_value': round(ltv, 2),
            'ltv_to_cac_ratio': round(ltv / cac, 2) if cac > 0 else 0,
            'payback_period_months': round((cac / (ltv / 36)), 1) if ltv > 0 else 0,  # 36 months assumed LTV period
            'customers_acquired': customers_acquired,
            'total_investment': total_spend,
            'acquisition_efficiency': self._grade_acquisition_efficiency(ltv / cac if cac > 0 else 0),
            'break_even_customers': int(total_spend / avg_order_value) if avg_order_value > 0 else 0,
            'profitability_threshold': self._calculate_profitability_threshold(cac, ltv),
            'scaling_potential': self._assess_scaling_potential(cac, ltv, total_spend),
            'benchmark_comparison': self._compare_to_benchmarks(cac, ltv),
            'optimization_insights': self._generate_cac_insights(cac, ltv, campaign_data),
            'timestamp': datetime.now().isoformat()
        }
        
        return metrics
    
    def compare_campaign_performance(self,
                                    campaigns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare performance across multiple campaigns.
        
        Args:
            campaigns: List of campaign data with performance metrics
            
        Returns:
            Comparative analysis across campaigns
        """
        if not campaigns:
            return {'error': 'No campaigns provided'}
        
        # Calculate metrics for each campaign
        campaign_metrics = []
        for campaign in campaigns:
            metrics = {
                'name': campaign.get('name', 'Unknown'),
                'roi': self._calculate_roi_percentage(
                    campaign.get('revenue', 0),
                    campaign.get('spend', 0)
                ),
                'roas': self._calculate_roas(
                    campaign.get('revenue', 0),
                    campaign.get('spend', 0)
                ),
                'cpl': self._safe_divide(campaign.get('spend', 0), campaign.get('leads', 0)),
                'conversion_rate': self._safe_divide(campaign.get('conversions', 0), campaign.get('leads', 0))
            }
            campaign_metrics.append(metrics)
        
        # Identify best and worst performers
        best_roi = max(campaign_metrics, key=lambda x: x['roi'])
        worst_roi = min(campaign_metrics, key=lambda x: x['roi'])
        best_roas = max(campaign_metrics, key=lambda x: x['roas'])
        
        comparison = {
            'campaigns_analyzed': len(campaigns),
            'campaign_metrics': campaign_metrics,
            'best_roi_campaign': best_roi,
            'worst_roi_campaign': worst_roi,
            'best_roas_campaign': best_roas,
            'average_roi': round(sum(c['roi'] for c in campaign_metrics) / len(campaign_metrics), 2),
            'average_roas': round(sum(c['roas'] for c in campaign_metrics) / len(campaign_metrics), 2),
            'performance_spread': round(best_roi['roi'] - worst_roi['roi'], 2),
            'insights': self._generate_comparison_insights(campaign_metrics),
            'recommendations': self._generate_comparison_recommendations(campaign_metrics),
            'timestamp': datetime.now().isoformat()
        }
        
        return comparison
    
    # Private helper methods
    
    def _load_industry_benchmarks(self) -> Dict[str, Any]:
        """Load industry benchmark data."""
        return {
            'roi': {
                'excellent': 500,  # 5:1 or better
                'good': 300,       # 3:1
                'average': 200,    # 2:1
                'poor': 100        # 1:1 (break even)
            },
            'cpl': {
                'B2B': 50,
                'B2C': 20,
                'SaaS': 75,
                'Ecommerce': 15
            },
            'cac': {
                'B2B': 200,
                'B2C': 100,
                'SaaS': 300,
                'Ecommerce': 50
            },
            'ltv_to_cac': {
                'excellent': 5.0,
                'good': 3.0,
                'acceptable': 2.0,
                'poor': 1.0
            }
        }
    
    def _calculate_roi_percentage(self, revenue: float, investment: float) -> float:
        """Calculate ROI percentage."""
        return self._safe_divide((revenue - investment), investment, 0) * 100
    
    def _calculate_roas(self, revenue: float, spend: float) -> float:
        """Calculate Return on Ad Spend."""
        return self._safe_divide(revenue, spend)
    
    def _grade_performance(self, roi: float, ltv_cac_ratio: float) -> str:
        """Grade overall campaign performance."""
        if roi >= 400 and ltv_cac_ratio >= 4:
            return "A+ (Excellent)"
        elif roi >= 300 and ltv_cac_ratio >= 3:
            return "A (Very Good)"
        elif roi >= 200 and ltv_cac_ratio >= 2:
            return "B (Good)"
        elif roi >= 100:
            return "C (Average)"
        elif roi >= 0:
            return "D (Below Average)"
        else:
            return "F (Poor)"
    
    def _generate_roi_insights(self, roi: float, roas: float, ltv_cac: float) -> List[str]:
        """Generate insights based on ROI metrics."""
        insights = []
        
        if roi >= 300:
            insights.append("Exceptional ROI performance - this campaign is highly profitable")
        elif roi >= 200:
            insights.append("Strong ROI - campaign is performing well above break-even")
        elif roi >= 100:
            insights.append("Positive ROI - campaign is profitable but has room for improvement")
        elif roi >= 0:
            insights.append("Break-even or slight loss - optimization needed")
        else:
            insights.append("Negative ROI - significant improvements required")
        
        if roas >= 5:
            insights.append("Outstanding ROAS - efficient revenue generation")
        elif roas >= 3:
            insights.append("Good ROAS - healthy return on ad spend")
        elif roas < 2:
            insights.append("ROAS below target - review targeting and creative")
        
        if ltv_cac >= 3:
            insights.append("Excellent LTV:CAC ratio - sustainable customer acquisition")
        elif ltv_cac >= 1.5:
            insights.append("Acceptable LTV:CAC ratio - monitor for improvements")
        elif ltv_cac > 0:
            insights.append("Low LTV:CAC ratio - focus on customer retention and value")
        
        return insights
    
    def _generate_roi_recommendations(self, campaign_data: Dict[str, Any], roi: float) -> List[str]:
        """Generate recommendations based on ROI performance."""
        recommendations = []
        
        if roi < 200:
            recommendations.append("Review and optimize underperforming channels")
            recommendations.append("Test new creative and messaging approaches")
            recommendations.append("Refine audience targeting to improve conversion")
        
        if roi >= 300:
            recommendations.append("Scale successful campaigns with increased budget")
            recommendations.append("Document winning strategies for future campaigns")
            recommendations.append("Test expansion into similar audiences")
        
        recommendations.append("Implement continuous A/B testing")
        recommendations.append("Monitor metrics weekly and adjust as needed")
        
        return recommendations
    
    def _classify_channel_performance(self, roi: float) -> str:
        """Classify channel performance into tiers."""
        if roi >= 400:
            return "Top Performer"
        elif roi >= 200:
            return "Strong Performer"
        elif roi >= 100:
            return "Average Performer"
        elif roi >= 0:
            return "Underperformer"
        else:
            return "Poor Performer"
    
    def _identify_best_channel(self, channel_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Identify the best performing channel."""
        if not channel_analysis:
            return {}
        
        best_channel = max(
            channel_analysis.items(),
            key=lambda x: x[1].get('roi_percentage', 0)
        )
        
        return {
            'channel': best_channel[0],
            'roi': best_channel[1].get('roi_percentage', 0),
            'reason': f"Highest ROI at {best_channel[1].get('roi_percentage', 0):.1f}%"
        }
    
    def _identify_worst_channel(self, channel_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Identify the worst performing channel."""
        if not channel_analysis:
            return {}
        
        worst_channel = min(
            channel_analysis.items(),
            key=lambda x: x[1].get('roi_percentage', 0)
        )
        
        return {
            'channel': worst_channel[0],
            'roi': worst_channel[1].get('roi_percentage', 0),
            'reason': f"Lowest ROI at {worst_channel[1].get('roi_percentage', 0):.1f}%"
        }
    
    def _identify_channel_optimizations(self, channel_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify optimization opportunities for channels."""
        opportunities = []
        
        for channel, data in channel_analysis.items():
            roi = data.get('roi_percentage', 0)
            if roi < 200:
                opportunities.append({
                    'channel': channel,
                    'opportunity': 'Improve targeting and creative',
                    'potential_impact': 'High'
                })
            
            conversion_rate = data.get('conversion_rate', 0)
            if conversion_rate < 0.02:  # Less than 2%
                opportunities.append({
                    'channel': channel,
                    'opportunity': 'Optimize landing pages and funnel',
                    'potential_impact': 'Medium'
                })
        
        return opportunities
    
    def _recommend_budget_shifts(self, channel_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommend budget shifts between channels."""
        recommendations = []
        
        # Find high and low performers
        sorted_channels = sorted(
            channel_analysis.items(),
            key=lambda x: x[1].get('roi_percentage', 0),
            reverse=True
        )
        
        if len(sorted_channels) >= 2:
            best = sorted_channels[0]
            worst = sorted_channels[-1]
            
            if best[1].get('roi_percentage', 0) > 300 and worst[1].get('roi_percentage', 0) < 100:
                recommendations.append({
                    'from': worst[0],
                    'to': best[0],
                    'amount': '20%',
                    'rationale': f"Shift budget from underperforming {worst[0]} to high-performing {best[0]}"
                })
        
        return recommendations
    
    def _allocate_based_on_performance(self,
                                      total_budget: float,
                                      channels: List[str],
                                      performance: Dict[str, Any]) -> Dict[str, float]:
        """Allocate budget based on historical performance."""
        allocation = {}
        
        # Calculate performance scores
        scores = {}
        total_score = 0
        for channel in channels:
            if channel in performance:
                # Use ROI as performance indicator
                score = max(0, performance[channel].get('roi_percentage', 100))
                scores[channel] = score
                total_score += score
            else:
                scores[channel] = 100  # Default score
                total_score += 100
        
        # Allocate proportionally with minimum floor
        min_allocation = total_budget * 0.05  # Minimum 5% per channel
        remaining_budget = total_budget - (min_allocation * len(channels))
        
        for channel in channels:
            proportion = scores[channel] / total_score if total_score > 0 else 1/len(channels)
            allocation[channel] = min_allocation + (remaining_budget * proportion)
        
        return allocation
    
    def _allocate_based_on_best_practices(self,
                                         total_budget: float,
                                         channels: List[str],
                                         objectives: List[str]) -> Dict[str, float]:
        """Allocate budget based on best practices."""
        # Default allocation percentages
        default_allocation = {
            'email': 0.10,
            'social_media': 0.20,
            'content': 0.20,
            'paid_ads': 0.35,
            'seo': 0.10,
            'events': 0.15,
            'pr': 0.10
        }
        
        # Adjust for objectives
        if 'brand_awareness' in [obj.lower() for obj in objectives]:
            default_allocation['social_media'] = 0.25
            default_allocation['pr'] = 0.15
            default_allocation['paid_ads'] = 0.30
        
        # Calculate for selected channels
        allocation = {}
        selected_total = sum(default_allocation.get(ch, 0.10) for ch in channels)
        
        for channel in channels:
            percentage = default_allocation.get(channel, 0.10) / selected_total
            allocation[channel] = round(total_budget * percentage, 2)
        
        return allocation
    
    def _calculate_expected_returns(self,
                                   allocation: Dict[str, float],
                                   performance: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate expected returns from allocation."""
        if not performance:
            # Use industry averages
            avg_roi = 200  # 2:1
            total_investment = sum(allocation.values())
            return {
                'total_investment': total_investment,
                'expected_revenue': total_investment * 2,
                'total_roi': avg_roi,
                'confidence': 'medium'
            }
        
        total_investment = sum(allocation.values())
        expected_revenue = 0
        
        for channel, budget in allocation.items():
            if channel in performance:
                channel_roi = performance[channel].get('roi_percentage', 200)
                expected_revenue += budget * (1 + channel_roi / 100)
            else:
                expected_revenue += budget * 2  # Default 2x return
        
        return {
            'total_investment': total_investment,
            'expected_revenue': round(expected_revenue, 2),
            'total_roi': round(((expected_revenue - total_investment) / total_investment * 100), 2),
            'confidence': 'high' if performance else 'medium'
        }
    
    def _calculate_confidence_level(self, performance: Optional[Dict[str, Any]]) -> str:
        """Calculate confidence level in allocation."""
        if not performance:
            return "Medium - Based on industry benchmarks"
        elif len(performance) >= 3:
            return "High - Based on substantial historical data"
        else:
            return "Medium - Based on limited historical data"
    
    def _explain_allocation_rationale(self,
                                     allocation: Dict[str, float],
                                     performance: Optional[Dict[str, Any]]) -> str:
        """Explain the rationale behind budget allocation."""
        if performance:
            return ("Budget allocated based on historical performance data, "
                   "with emphasis on high-ROI channels while maintaining "
                   "minimum investment across all channels for testing.")
        else:
            return ("Budget allocated based on industry best practices and "
                   "typical channel performance, with flexibility for optimization "
                   "as performance data becomes available.")
    
    def _define_optimization_strategy(self, objectives: List[str]) -> str:
        """Define the optimization strategy."""
        if 'awareness' in str(objectives).lower():
            return "Focus on reach and engagement metrics, optimize for brand lift"
        elif 'lead' in str(objectives).lower():
            return "Focus on lead volume and quality, optimize for cost per lead"
        else:
            return "Focus on revenue and ROI, optimize for customer acquisition cost"
    
    def _get_benchmark_roi(self, objective: str, channels: List[str]) -> float:
        """Get benchmark ROI for objective and channels."""
        base_roi = 200  # 2:1 default
        
        # Adjust based on channels
        if 'paid_ads' in channels:
            base_roi += 50
        if 'email' in channels:
            base_roi += 30
        if 'content' in channels:
            base_roi += 20
        
        # Adjust based on objective
        if 'awareness' in objective.lower():
            base_roi -= 50  # Awareness campaigns typically lower immediate ROI
        elif 'retention' in objective.lower():
            base_roi += 100  # Retention campaigns typically higher ROI
        
        return base_roi
    
    def _calculate_market_adjustment(self, conditions: Dict[str, Any]) -> float:
        """Calculate market condition adjustment factor."""
        factor = 1.0
        
        if conditions.get('competition') == 'high':
            factor *= 0.9
        elif conditions.get('competition') == 'low':
            factor *= 1.1
        
        if conditions.get('seasonality') == 'peak':
            factor *= 1.2
        elif conditions.get('seasonality') == 'off':
            factor *= 0.8
        
        if conditions.get('economic_climate') == 'favorable':
            factor *= 1.1
        elif conditions.get('economic_climate') == 'challenging':
            factor *= 0.9
        
        return factor
    
    def _calculate_confidence_intervals(self, predicted_roi: float) -> Dict[str, float]:
        """Calculate confidence intervals for prediction."""
        return {
            'low': round(predicted_roi * 0.7, 2),
            'expected': round(predicted_roi, 2),
            'high': round(predicted_roi * 1.3, 2)
        }
    
    def _estimate_leads(self, budget: float, channels: List[str]) -> float:
        """Estimate number of leads."""
        # Average cost per lead varies by channel
        avg_cpl = 40
        
        if 'paid_ads' in channels:
            avg_cpl = 35
        if 'content' in channels:
            avg_cpl = 45
        
        return budget / avg_cpl
    
    def _estimate_customers(self, leads: float, objective: str) -> float:
        """Estimate number of customers from leads."""
        # Average conversion rate from lead to customer
        if 'acquisition' in objective.lower():
            conversion_rate = 0.15  # 15%
        else:
            conversion_rate = 0.10  # 10%
        
        return leads * conversion_rate
    
    def _assess_campaign_risk(self, campaign_plan: Dict[str, Any]) -> Dict[str, str]:
        """Assess risk level of campaign."""
        budget = campaign_plan.get('budget', 0)
        
        risk_level = 'Medium'
        if budget > 100000:
            risk_level = 'High'
        elif budget < 10000:
            risk_level = 'Low'
        
        return {
            'overall_risk': risk_level,
            'budget_risk': 'High' if budget > 100000 else 'Low',
            'execution_risk': 'Medium',
            'market_risk': 'Medium'
        }
    
    def _calculate_success_probability(self, campaign_plan: Dict[str, Any]) -> float:
        """Calculate probability of campaign success."""
        # Base probability
        probability = 0.65
        
        # Adjust based on budget (more budget = slight increase)
        budget = campaign_plan.get('budget', 0)
        if budget > 50000:
            probability += 0.10
        
        # Adjust based on number of channels (diversification)
        channels = campaign_plan.get('channels', [])
        if len(channels) >= 3:
            probability += 0.05
        
        return round(min(probability, 0.95), 2)  # Cap at 95%
    
    def _list_key_assumptions(self, campaign_plan: Dict[str, Any]) -> List[str]:
        """List key assumptions in prediction."""
        return [
            "Historical performance patterns continue",
            "Market conditions remain stable",
            "Target audience behavior consistent",
            "Competitive landscape unchanged",
            "Budget fully deployed as planned"
        ]
    
    def _perform_sensitivity_analysis(self, budget: float, roi: float) -> Dict[str, Any]:
        """Perform sensitivity analysis on key variables."""
        return {
            'budget_impact': {
                '-20%': round(budget * 0.8 * (roi / 100), 2),
                'baseline': round(budget * (roi / 100), 2),
                '+20%': round(budget * 1.2 * (roi / 100), 2)
            },
            'roi_impact': {
                '-20%': round(budget * (roi * 0.8 / 100), 2),
                'baseline': round(budget * (roi / 100), 2),
                '+20%': round(budget * (roi * 1.2 / 100), 2)
            }
        }
    
    def _calculate_efficiency_score(self, channel: str, spend: float, results: Dict[str, Any]) -> float:
        """Calculate efficiency score for a channel."""
        # Simple efficiency score based on results vs spend
        revenue = results.get('revenue', {}).get(channel, 0)
        if spend == 0:
            return 0
        
        efficiency = (revenue / spend) * 100
        return round(min(efficiency, 100), 1)  # Cap at 100
    
    def _calculate_overall_efficiency(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall budget efficiency."""
        scores = [data['efficiency_score'] for data in metrics.values()]
        if not scores:
            return 0
        return round(sum(scores) / len(scores), 1)
    
    def _assess_budget_discipline(self, actual: Dict[str, float], planned: Dict[str, float]) -> str:
        """Assess budget discipline."""
        total_variance = sum(abs(actual.get(ch, 0) - planned.get(ch, 0)) for ch in planned)
        total_planned = sum(planned.values())
        
        variance_percentage = (total_variance / total_planned * 100) if total_planned > 0 else 0
        
        if variance_percentage < 5:
            return "Excellent - Stayed within 5% of plan"
        elif variance_percentage < 10:
            return "Good - Stayed within 10% of plan"
        elif variance_percentage < 20:
            return "Fair - Some variance from plan"
        else:
            return "Poor - Significant deviation from plan"
    
    def _analyze_spending_patterns(self, spend: Dict[str, float]) -> Dict[str, Any]:
        """Analyze spending patterns."""
        total = sum(spend.values())
        
        return {
            'total_spend': round(total, 2),
            'distribution': {ch: round((amt/total*100), 1) for ch, amt in spend.items()},
            'concentration': 'Balanced' if max(spend.values()) / total < 0.4 else 'Concentrated'
        }
    
    def _identify_waste(self, metrics: Dict[str, Any], results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify potential waste in budget."""
        waste = []
        
        for channel, data in metrics.items():
            if data['efficiency_score'] < 30:
                waste.append({
                    'channel': channel,
                    'issue': 'Low efficiency score',
                    'amount': f"${data['actual']:.2f}",
                    'recommendation': 'Consider reducing or optimizing'
                })
        
        return waste
    
    def _generate_efficiency_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate efficiency improvement recommendations."""
        recommendations = []
        
        for channel, data in metrics.items():
            if data['efficiency_score'] < 50:
                recommendations.append(f"Optimize {channel} - current efficiency at {data['efficiency_score']}%")
        
        if not recommendations:
            recommendations.append("Maintain current efficient operations")
            recommendations.append("Look for incremental optimization opportunities")
        
        return recommendations
    
    def _suggest_reallocation(self, metrics: Dict[str, Any], results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Suggest budget reallocation."""
        suggestions = []
        
        # Find channels to reduce
        for channel, data in metrics.items():
            if data['efficiency_score'] < 40:
                suggestions.append({
                    'action': 'reduce',
                    'channel': channel,
                    'amount': '25%',
                    'reason': 'Low efficiency score'
                })
        
        return suggestions
    
    def _grade_acquisition_efficiency(self, ltv_cac_ratio: float) -> str:
        """Grade customer acquisition efficiency."""
        if ltv_cac_ratio >= 5:
            return "A+ (Excellent)"
        elif ltv_cac_ratio >= 3:
            return "A (Very Good)"
        elif ltv_cac_ratio >= 2:
            return "B (Good)"
        elif ltv_cac_ratio >= 1:
            return "C (Acceptable)"
        else:
            return "D (Poor)"
    
    def _calculate_profitability_threshold(self, cac: float, ltv: float) -> Dict[str, Any]:
        """Calculate profitability threshold."""
        return {
            'break_even_ratio': '1:1 (LTV:CAC)',
            'current_ratio': f"{(ltv/cac if cac > 0 else 0):.1f}:1",
            'target_ratio': '3:1 or better',
            'status': 'Profitable' if ltv > cac else 'Unprofitable'
        }
    
    def _assess_scaling_potential(self, cac: float, ltv: float, spend: float) -> str:
        """Assess potential for scaling."""
        if ltv / cac >= 3 if cac > 0 else False:
            return "High - Strong unit economics support scaling"
        elif ltv / cac >= 2 if cac > 0 else False:
            return "Medium - Can scale with optimization"
        else:
            return "Low - Improve efficiency before scaling"
    
    def _compare_to_benchmarks(self, cac: float, ltv: float) -> Dict[str, str]:
        """Compare metrics to industry benchmarks."""
        benchmarks = self.benchmarks
        
        return {
            'cac_vs_benchmark': 'Above average' if cac < 200 else 'Below average',
            'ltv_vs_benchmark': 'Strong' if ltv > 500 else 'Needs improvement',
            'ratio_vs_benchmark': 'Excellent' if (ltv/cac if cac > 0 else 0) >= 3 else 'Fair'
        }
    
    def _generate_cac_insights(self, cac: float, ltv: float, data: Dict[str, Any]) -> List[str]:
        """Generate CAC optimization insights."""
        insights = []
        
        if cac > 200:
            insights.append("CAC is high - optimize targeting and conversion funnel")
        
        if ltv < cac * 3:
            insights.append("Focus on increasing customer lifetime value")
        
        insights.append("Monitor payback period and cash flow implications")
        insights.append("Test retention strategies to improve LTV")
        
        return insights
    
    def _generate_comparison_insights(self, metrics: List[Dict[str, Any]]) -> List[str]:
        """Generate insights from campaign comparison."""
        insights = []
        
        roi_values = [m['roi'] for m in metrics]
        avg_roi = sum(roi_values) / len(roi_values)
        
        if max(roi_values) > avg_roi * 2:
            insights.append("Significant performance variance - investigate top performers")
        
        if min(roi_values) < 0:
            insights.append("Some campaigns losing money - immediate optimization needed")
        
        insights.append(f"Average ROI across campaigns: {avg_roi:.1f}%")
        
        return insights
    
    def _generate_comparison_recommendations(self, metrics: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations from campaign comparison."""
        return [
            "Scale budget for top-performing campaigns",
            "Pause or optimize poor-performing campaigns",
            "Apply learnings from winners to other campaigns",
            "Conduct detailed analysis of performance differences"
        ]
    
    def get_all_calculations(self) -> List[Dict[str, Any]]:
        """Get all ROI calculations."""
        return self.calculations
    
    def export_calculation(self, index: int = -1) -> str:
        """Export a calculation as JSON string."""
        if not self.calculations:
            return json.dumps({'error': 'No calculations available'})
        
        calculation = self.calculations[index]
        return json.dumps(calculation, indent=2)
