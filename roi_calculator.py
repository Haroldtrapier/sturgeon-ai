"""
ROI CALCULATOR MODULE
Calculate marketing ROI, optimize budgets, and project growth trajectories
"""


class ROICalculator:
    """Calculate marketing ROI and optimize budget allocation"""
    
    def __init__(self):
        # Channel performance benchmarks
        self.channel_metrics = {
            'linkedin_ads': {
                'cpm': 35.0,  # Cost per 1000 impressions
                'ctr': 0.022,  # Click-through rate
                'cpc': 8.50,  # Cost per click
                'conversion_rate': 0.025,  # Lead conversion rate
                'avg_deal_size': 5000,
                'sales_cycle_months': 3,
                'close_rate': 0.20
            },
            'content_marketing': {
                'cost_per_article': 500,
                'articles_per_month': 4,
                'avg_monthly_traffic': 2000,
                'lead_conversion_rate': 0.03,
                'avg_deal_size': 5000,
                'sales_cycle_months': 4,
                'close_rate': 0.15
            },
            'email_marketing': {
                'cost_per_campaign': 200,
                'campaigns_per_month': 4,
                'list_size': 1000,
                'open_rate': 0.25,
                'click_rate': 0.08,
                'conversion_rate': 0.05,
                'avg_deal_size': 5000,
                'sales_cycle_months': 2,
                'close_rate': 0.25
            },
            'google_ads': {
                'cpc': 12.0,
                'ctr': 0.035,
                'conversion_rate': 0.03,
                'avg_deal_size': 5000,
                'sales_cycle_months': 2,
                'close_rate': 0.18
            },
            'seo': {
                'monthly_cost': 2000,
                'ramp_up_months': 6,
                'mature_monthly_traffic': 5000,
                'lead_conversion_rate': 0.025,
                'avg_deal_size': 5000,
                'sales_cycle_months': 4,
                'close_rate': 0.15
            }
        }
        
        # Business metrics
        self.avg_customer_lifetime_value = 25000
        self.avg_monthly_recurring_revenue = 149
        self.churn_rate_monthly = 0.05
    
    def calculate_campaign_roi(self, channel, budget, duration_months=3):
        """
        Calculate expected ROI for a marketing campaign
        
        Args:
            channel: Marketing channel (e.g., 'linkedin_ads')
            budget: Total campaign budget
            duration_months: Campaign duration in months
            
        Returns:
            ROI analysis with performance metrics and recommendations
        """
        if channel not in self.channel_metrics:
            raise ValueError(f"Unknown channel: {channel}. Available: {list(self.channel_metrics.keys())}")
        
        metrics = self.channel_metrics[channel]
        monthly_spend = budget / duration_months
        
        # Calculate performance based on channel type
        if channel == 'linkedin_ads':
            total_clicks = budget / metrics['cpc']
            total_leads = total_clicks * metrics['conversion_rate']
            total_customers = total_leads * metrics['close_rate']
            
        elif channel == 'content_marketing':
            total_articles = metrics['articles_per_month'] * duration_months
            total_traffic = metrics['avg_monthly_traffic'] * duration_months
            total_leads = total_traffic * metrics['lead_conversion_rate']
            total_customers = total_leads * metrics['close_rate']
            
        elif channel == 'email_marketing':
            total_campaigns = metrics['campaigns_per_month'] * duration_months
            total_opens = total_campaigns * metrics['list_size'] * metrics['open_rate']
            total_clicks = total_opens * metrics['click_rate']
            total_leads = total_clicks * metrics['conversion_rate']
            total_customers = total_leads * metrics['close_rate']
            
        elif channel == 'google_ads':
            total_clicks = budget / metrics['cpc']
            total_leads = total_clicks * metrics['conversion_rate']
            total_customers = total_leads * metrics['close_rate']
            
        elif channel == 'seo':
            # SEO has ramp-up period
            if duration_months <= metrics['ramp_up_months']:
                traffic_multiplier = duration_months / metrics['ramp_up_months']
            else:
                traffic_multiplier = 1.0
            total_traffic = metrics['mature_monthly_traffic'] * duration_months * traffic_multiplier
            total_leads = total_traffic * metrics['lead_conversion_rate']
            total_customers = total_leads * metrics['close_rate']
        
        else:
            total_leads = 0
            total_customers = 0
        
        # Calculate revenue and ROI
        total_revenue = total_customers * metrics['avg_deal_size']
        lifetime_value = total_customers * self.avg_customer_lifetime_value
        net_profit = total_revenue - budget
        roi_percentage = (net_profit / budget * 100) if budget > 0 else 0
        
        # Calculate efficiency metrics
        cost_per_lead = budget / total_leads if total_leads > 0 else 0
        cost_per_customer = budget / total_customers if total_customers > 0 else 0
        customer_lifetime_value_ratio = self.avg_customer_lifetime_value / cost_per_customer if cost_per_customer > 0 else 0
        payback_period_months = cost_per_customer / self.avg_monthly_recurring_revenue if self.avg_monthly_recurring_revenue > 0 else 0
        
        # Generate recommendation
        if roi_percentage > 200:
            recommendation = f"Excellent ROI! Consider increasing budget for {channel} by 50-100%."
        elif roi_percentage > 100:
            recommendation = f"Strong performance. {channel.replace('_', ' ').title()} is a profitable channel."
        elif roi_percentage > 0:
            recommendation = f"Positive ROI but room for improvement. Optimize targeting and messaging."
        else:
            recommendation = f"Negative ROI. Consider pausing {channel} and testing different approach."
        
        return {
            'channel': channel,
            'investment': {
                'budget': budget,
                'duration_months': duration_months,
                'monthly_spend': monthly_spend
            },
            'performance': {
                'total_leads': int(total_leads),
                'total_customers': int(total_customers),
                'total_revenue': total_revenue,
                'lifetime_value': lifetime_value
            },
            'efficiency_metrics': {
                'cost_per_lead': cost_per_lead,
                'cost_per_customer': cost_per_customer,
                'ltv_to_cac_ratio': customer_lifetime_value_ratio,
                'payback_period_months': payback_period_months
            },
            'returns': {
                'net_profit': net_profit,
                'roi_percentage': roi_percentage,
                'return_multiple': (total_revenue / budget) if budget > 0 else 0
            },
            'recommendation': recommendation
        }
    
    def optimize_budget_allocation(self, total_budget, channels):
        """
        Optimize budget allocation across multiple channels
        
        Args:
            total_budget: Total marketing budget to allocate
            channels: List of channels to consider
            
        Returns:
            Optimized allocation with expected results per channel
        """
        # Calculate ROI efficiency score for each channel
        channel_scores = {}
        for channel in channels:
            if channel not in self.channel_metrics:
                continue
            
            # Use a test budget to calculate efficiency
            test_budget = 1000
            test_roi = self.calculate_campaign_roi(channel, test_budget, 1)
            
            # Score based on multiple factors
            efficiency_score = (
                test_roi['returns']['roi_percentage'] * 0.4 +  # ROI weight
                (test_roi['efficiency_metrics']['ltv_to_cac_ratio'] * 20) * 0.3 +  # LTV:CAC weight
                (test_roi['performance']['total_customers'] / (test_budget / 1000)) * 100 * 0.3  # Customers per $1K weight
            )
            channel_scores[channel] = efficiency_score
        
        # Normalize scores to get allocation percentages
        total_score = sum(channel_scores.values())
        allocations = {
            channel: (score / total_score) 
            for channel, score in channel_scores.items()
        }
        
        # Calculate expected results for each channel
        optimized_allocation = {}
        total_customers = 0
        total_revenue = 0
        
        for channel, percentage in allocations.items():
            channel_budget = total_budget * percentage
            channel_roi = self.calculate_campaign_roi(channel, channel_budget, 3)
            
            optimized_allocation[channel] = {
                'budget': channel_budget,
                'percentage': int(percentage * 100),
                'expected_customers': channel_roi['performance']['total_customers'],
                'expected_revenue': channel_roi['performance']['total_revenue'],
                'roi': channel_roi['returns']['roi_percentage']
            }
            
            total_customers += channel_roi['performance']['total_customers']
            total_revenue += channel_roi['performance']['total_revenue']
        
        # Generate execution priority
        sorted_channels = sorted(
            optimized_allocation.items(),
            key=lambda x: x[1]['roi'],
            reverse=True
        )
        
        execution_priority = [
            f"1. Start with {sorted_channels[0][0].replace('_', ' ').title()} (highest ROI: {sorted_channels[0][1]['roi']:.1f}%)",
            f"2. Scale {sorted_channels[1][0].replace('_', ' ').title()} after validating results",
            f"3. Add {sorted_channels[2][0].replace('_', ' ').title()} for diversification" if len(sorted_channels) > 2 else ""
        ]
        
        weighted_avg_roi = (total_revenue - total_budget) / total_budget * 100 if total_budget > 0 else 0
        
        return {
            'total_budget': total_budget,
            'optimized_allocation': optimized_allocation,
            'total_expected_results': {
                'total_customers': int(total_customers),
                'total_revenue': total_revenue,
                'weighted_average_roi': weighted_avg_roi
            },
            'execution_priority': execution_priority,
            'diversification_note': 'Budget is split based on ROI efficiency. Start with highest ROI channel and scale.'
        }
    
    def project_growth_trajectory(self, monthly_budget, duration_months=12):
        """
        Project 12-month growth trajectory with given budget
        
        Args:
            monthly_budget: Monthly marketing budget
            duration_months: Projection period (default 12 months)
            
        Returns:
            Month-by-month growth projection with key milestones
        """
        # Optimal channel allocation for sustainable growth
        channel_allocation = {
            'linkedin_ads': 0.35,
            'content_marketing': 0.30,
            'email_marketing': 0.20,
            'seo': 0.15
        }
        
        # Calculate monthly performance
        monthly_breakdown = []
        cumulative_customers = 0
        cumulative_revenue = 0
        
        for month in range(1, duration_months + 1):
            month_customers = 0
            month_revenue = 0
            
            # Calculate customers from each channel
            for channel, allocation in channel_allocation.items():
                channel_budget = monthly_budget * allocation
                
                # Adjust for learning curve (efficiency improves over time)
                efficiency_multiplier = min(1.0, 0.5 + (month / duration_months) * 0.5)
                adjusted_budget = channel_budget * efficiency_multiplier
                
                channel_result = self.calculate_campaign_roi(channel, adjusted_budget, 1)
                month_customers += channel_result['performance']['total_customers']
                month_revenue += channel_result['performance']['total_revenue']
            
            cumulative_customers += month_customers
            cumulative_revenue += month_revenue
            
            # Calculate MRR (assuming SaaS model)
            mrr = cumulative_customers * self.avg_monthly_recurring_revenue * (1 - self.churn_rate_monthly) ** month
            
            monthly_breakdown.append({
                'month': month,
                'spend': monthly_budget,
                'customers': int(month_customers),
                'cumulative_customers': int(cumulative_customers),
                'mrr': mrr,
                'revenue': month_revenue,
                'cumulative_revenue': cumulative_revenue
            })
        
        # Calculate key milestones
        total_investment = monthly_budget * duration_months
        final_month = monthly_breakdown[-1]
        
        # Find break-even month
        break_even_month = 0
        for i, month_data in enumerate(monthly_breakdown):
            if month_data['cumulative_revenue'] >= (i + 1) * monthly_budget:
                break_even_month = i + 1
                break
        
        # Find profitability month (MRR > monthly marketing spend)
        profitable_month = 0
        for i, month_data in enumerate(monthly_breakdown):
            if month_data['mrr'] >= monthly_budget:
                profitable_month = i + 1
                break
        
        return {
            'monthly_budget': monthly_budget,
            'total_investment': total_investment,
            'projection_period': f'{duration_months} months',
            'channel_allocation': channel_allocation,
            'monthly_breakdown': monthly_breakdown,
            'year_end_totals': {
                'total_customers': final_month['cumulative_customers'],
                'total_revenue': final_month['cumulative_revenue'],
                'final_mrr': final_month['mrr'],
                'total_roi': ((final_month['cumulative_revenue'] - total_investment) / total_investment * 100)
            },
            'key_milestones': {
                'break_even_month': break_even_month,
                'profitable_mrr_month': profitable_month,
                'months_to_100_customers': next((m['month'] for m in monthly_breakdown if m['cumulative_customers'] >= 100), 0)
            },
            'strategic_insights': [
                'Growth accelerates after month 3 as channels optimize',
                'MRR compounds over time due to customer retention',
                'Consider increasing budget after validating channel performance',
                'Focus on customer success to maintain low churn rate'
            ]
        }


# Create singleton instance
roi_calc = ROICalculator()
