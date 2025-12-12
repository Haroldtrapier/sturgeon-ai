#!/usr/bin/env python3
"""
ROI Calculator Module for Sturgeon AI Marketing Director
Calculates campaign ROI, optimizes budget allocation, and projects growth trajectories
"""


class ROICalculator:
    """Marketing ROI calculator with industry benchmarks and projections"""
    
    # Configuration constants
    VIRAL_COEFFICIENT = 0.05  # 5% monthly viral growth from existing customer base
    MONTHLY_SUBSCRIPTION_VALUE = 200  # Monthly subscription value (MRR per customer)
    ALLOCATION_STRATEGY = [0.50, 0.30, 0.20]  # Budget allocation for top 3 channels
    CUSTOMER_RETENTION_YEARS = 2  # Average customer retention period
    ROI_TEST_BUDGET = 1000  # Standard budget for relative ROI testing
    ROI_TEST_DURATION = 3  # Standard duration in months for ROI testing
    
    # Industry benchmarks for different channels
    CHANNEL_BENCHMARKS = {
        'linkedin_ads': {
            'cpm': 75,  # Cost per 1000 impressions
            'ctr': 0.025,  # Click-through rate
            'conversion_rate': 0.08,  # Lead to customer
            'avg_customer_value': 2400,  # Annual contract value
            'sales_cycle_months': 3
        },
        'content_marketing': {
            'cost_per_article': 500,
            'articles_per_month': 4,
            'traffic_per_article': 500,
            'conversion_rate': 0.03,
            'avg_customer_value': 2400,
            'sales_cycle_months': 4
        },
        'email_marketing': {
            'cost_per_send': 0.05,
            'sends_per_month': 10000,
            'open_rate': 0.25,
            'click_rate': 0.12,
            'conversion_rate': 0.06,
            'avg_customer_value': 2400,
            'sales_cycle_months': 2
        },
        'google_ads': {
            'cpc': 8.5,  # Cost per click
            'conversion_rate': 0.05,
            'avg_customer_value': 2400,
            'sales_cycle_months': 3
        }
    }
    
    def calculate_campaign_roi(self, channel, budget, duration_months):
        """
        Calculate expected ROI for a marketing campaign
        
        Args:
            channel: Marketing channel (e.g., 'linkedin_ads')
            budget: Total campaign budget
            duration_months: Campaign duration in months
            
        Returns:
            dict: Complete ROI analysis with projections and recommendations
        """
        if channel not in self.CHANNEL_BENCHMARKS:
            raise ValueError(f"Unknown channel: {channel}. Available: {list(self.CHANNEL_BENCHMARKS.keys())}")
        
        benchmarks = self.CHANNEL_BENCHMARKS[channel]
        monthly_spend = budget / duration_months
        
        # Calculate performance metrics based on channel type
        if channel == 'linkedin_ads':
            impressions = (budget / benchmarks['cpm']) * 1000
            clicks = impressions * benchmarks['ctr']
            customers = clicks * benchmarks['conversion_rate']
            
        elif channel == 'content_marketing':
            total_articles = benchmarks['articles_per_month'] * duration_months
            total_traffic = total_articles * benchmarks['traffic_per_article']
            customers = total_traffic * benchmarks['conversion_rate']
            
        elif channel == 'email_marketing':
            total_sends = benchmarks['sends_per_month'] * duration_months
            opens = total_sends * benchmarks['open_rate']
            clicks = opens * benchmarks['click_rate']
            customers = clicks * benchmarks['conversion_rate']
            
        elif channel == 'google_ads':
            clicks = budget / benchmarks['cpc']
            customers = clicks * benchmarks['conversion_rate']
        
        # Calculate revenue and ROI
        total_revenue = customers * benchmarks['avg_customer_value']
        profit = total_revenue - budget
        roi_percentage = (profit / budget) * 100 if budget > 0 else 0
        roi_multiple = total_revenue / budget if budget > 0 else 0
        
        # Calculate efficiency metrics
        cost_per_customer = budget / customers if customers > 0 else 0
        customer_lifetime_value = benchmarks['avg_customer_value'] * self.CUSTOMER_RETENTION_YEARS
        ltv_cac_ratio = customer_lifetime_value / cost_per_customer if cost_per_customer > 0 else 0
        payback_months = cost_per_customer / (benchmarks['avg_customer_value'] / 12) if benchmarks['avg_customer_value'] > 0 else 0
        
        # Generate recommendation
        if roi_percentage > 200:
            recommendation = f"Excellent ROI! Consider increasing budget allocation to {channel.replace('_', ' ')} for maximum growth."
        elif roi_percentage > 100:
            recommendation = f"Strong positive ROI. {channel.replace('_', ' ').title()} is performing well and should be maintained."
        elif roi_percentage > 0:
            recommendation = f"Modest positive ROI. Consider optimizing {channel.replace('_', ' ')} campaigns or testing alternative channels."
        else:
            recommendation = f"Negative ROI. Recommend pausing {channel.replace('_', ' ')} and reallocating budget to higher-performing channels."
        
        return {
            'channel': channel,
            'investment': {
                'budget': budget,
                'duration_months': duration_months,
                'monthly_spend': monthly_spend
            },
            'performance': {
                'customers_acquired': int(customers),
                'total_revenue': total_revenue,
                'profit': profit
            },
            'efficiency_metrics': {
                'cost_per_customer': cost_per_customer,
                'ltv_cac_ratio': ltv_cac_ratio,
                'payback_months': payback_months
            },
            'returns': {
                'roi_percentage': roi_percentage,
                'roi_multiple': roi_multiple,
                'total_revenue': total_revenue,
                'net_profit': profit
            },
            'recommendation': recommendation
        }
    
    def optimize_budget_allocation(self, total_budget, channels):
        """
        Optimize budget allocation across multiple marketing channels
        
        Args:
            total_budget: Total available marketing budget
            channels: List of channel names to allocate budget to
            
        Returns:
            dict: Optimized allocation with expected results per channel
        """
        # Calculate ROI potential for each channel using standard test parameters
        channel_rois = {}
        for channel in channels:
            if channel in self.CHANNEL_BENCHMARKS:
                test_roi = self.calculate_campaign_roi(channel, self.ROI_TEST_BUDGET, self.ROI_TEST_DURATION)
                channel_rois[channel] = test_roi['returns']['roi_percentage']
        
        # Sort channels by ROI
        sorted_channels = sorted(channel_rois.items(), key=lambda x: x[1], reverse=True)
        
        # Validate channel count and adjust allocation
        if len(sorted_channels) > len(self.ALLOCATION_STRATEGY):
            sorted_channels = sorted_channels[:len(self.ALLOCATION_STRATEGY)]
        
        # Allocate budget proportionally based on number of channels available
        allocation_percentages = self.ALLOCATION_STRATEGY[:len(sorted_channels)]
        # Normalize percentages to sum to 1.0 if we have fewer channels
        total_allocated = sum(allocation_percentages)
        if total_allocated < 1.0 and len(allocation_percentages) > 0:
            # Redistribute remaining budget proportionally
            scaling_factor = 1.0 / total_allocated
            allocation_percentages = [p * scaling_factor for p in allocation_percentages]
        
        optimized_allocation = {}
        total_customers = 0
        total_revenue = 0
        
        for i, (channel, roi) in enumerate(sorted_channels):
            if i >= len(allocation_percentages):
                break
                
            percentage = allocation_percentages[i]
            channel_budget = total_budget * percentage
            
            # Calculate expected results for this allocation
            results = self.calculate_campaign_roi(channel, channel_budget, 3)
            
            optimized_allocation[channel] = {
                'budget': channel_budget,
                'percentage': int(percentage * 100),
                'expected_customers': results['performance']['customers_acquired'],
                'expected_revenue': results['performance']['total_revenue'],
                'roi': results['returns']['roi_percentage']
            }
            
            total_customers += results['performance']['customers_acquired']
            total_revenue += results['performance']['total_revenue']
        
        # Calculate blended metrics
        blended_roi = ((total_revenue - total_budget) / total_budget) * 100 if total_budget > 0 else 0
        
        # Generate execution priority based on number of channels
        execution_priority = []
        if len(sorted_channels) >= 1:
            execution_priority.append(f"1. Launch {sorted_channels[0][0].replace('_', ' ')} campaign first (highest ROI: {sorted_channels[0][1]:.1f}%)")
        if len(sorted_channels) >= 2:
            execution_priority.append(f"2. Scale {sorted_channels[1][0].replace('_', ' ')} campaign after week 2")
        if len(sorted_channels) >= 3:
            execution_priority.append(f"3. Add {sorted_channels[2][0].replace('_', ' ')} for channel diversification by week 4")
        execution_priority.extend([
            f"{len(sorted_channels) + 1}. Monitor metrics weekly and reallocate budget based on performance",
            f"{len(sorted_channels) + 2}. A/B test within each channel to improve conversion rates"
        ])
        
        return {
            'total_budget': total_budget,
            'optimized_allocation': optimized_allocation,
            'total_expected_results': {
                'total_customers': int(total_customers),
                'total_revenue': total_revenue,
                'blended_roi': blended_roi
            },
            'execution_priority': execution_priority
        }
    
    def project_growth_trajectory(self, monthly_budget, duration_months):
        """
        Project company growth over time with given marketing budget
        
        Args:
            monthly_budget: Monthly marketing budget
            duration_months: Projection period in months
            
        Returns:
            dict: Month-by-month growth projections with key milestones
        """
        # Default channel allocation for balanced growth
        channel_allocation = {
            'linkedin_ads': 0.40,
            'content_marketing': 0.30,
            'email_marketing': 0.30
        }
        
        monthly_breakdown = []
        cumulative_customers = 0
        cumulative_revenue = 0
        cumulative_investment = 0
        
        # Use class-defined viral coefficient for compounding growth
        viral_coefficient = self.VIRAL_COEFFICIENT
        
        for month in range(1, duration_months + 1):
            month_customers = 0
            month_revenue = 0
            
            # Calculate customers from each channel
            for channel, allocation in channel_allocation.items():
                channel_budget = monthly_budget * allocation
                
                # Calculate monthly customer acquisition
                benchmarks = self.CHANNEL_BENCHMARKS[channel]
                
                if channel == 'linkedin_ads':
                    impressions = (channel_budget / benchmarks['cpm']) * 1000
                    clicks = impressions * benchmarks['ctr']
                    customers = clicks * benchmarks['conversion_rate']
                    
                elif channel == 'content_marketing':
                    traffic = benchmarks['traffic_per_article'] * benchmarks['articles_per_month']
                    customers = traffic * benchmarks['conversion_rate']
                    
                elif channel == 'email_marketing':
                    sends = benchmarks['sends_per_month']
                    opens = sends * benchmarks['open_rate']
                    clicks = opens * benchmarks['click_rate']
                    customers = clicks * benchmarks['conversion_rate']
                
                month_customers += customers
            
            # Add viral/referral customers (compounding effect)
            viral_customers = cumulative_customers * viral_coefficient
            month_customers += viral_customers
            
            # Update cumulative customers
            cumulative_customers += month_customers
            
            # Calculate revenue (Monthly Recurring Revenue model)
            avg_customer_value = self.MONTHLY_SUBSCRIPTION_VALUE
            month_revenue = cumulative_customers * avg_customer_value
            cumulative_revenue += month_revenue
            cumulative_investment += monthly_budget
            
            monthly_breakdown.append({
                'month': month,
                'customers': int(month_customers),
                'cumulative_customers': int(cumulative_customers),
                'mrr': month_revenue,
                'cumulative_revenue': cumulative_revenue,
                'investment': monthly_budget,
                'cumulative_investment': cumulative_investment
            })
        
        # Calculate year-end metrics
        total_investment = monthly_budget * duration_months
        final_month_mrr = monthly_breakdown[-1]['mrr']
        annual_recurring_revenue = final_month_mrr * 12
        roi_percentage = ((cumulative_revenue - total_investment) / total_investment) * 100 if total_investment > 0 else 0
        
        # Identify key milestones
        milestone_10_customers = next((m['month'] for m in monthly_breakdown if m['cumulative_customers'] >= 10), 0)
        milestone_50_customers = next((m['month'] for m in monthly_breakdown if m['cumulative_customers'] >= 50), 0)
        milestone_100_customers = next((m['month'] for m in monthly_breakdown if m['cumulative_customers'] >= 100), 0)
        milestone_break_even = next((m['month'] for m in monthly_breakdown if m['cumulative_revenue'] >= m['cumulative_investment']), 0)
        
        return {
            'monthly_budget': monthly_budget,
            'total_investment': total_investment,
            'projection_period': f'{duration_months} months',
            'channel_allocation': channel_allocation,
            'monthly_breakdown': monthly_breakdown,
            'year_end_totals': {
                'total_customers': int(cumulative_customers),
                'mrr': final_month_mrr,
                'arr': annual_recurring_revenue,
                'total_revenue': cumulative_revenue,
                'roi_percentage': roi_percentage
            },
            'key_milestones': {
                'first_10_customers': milestone_10_customers,
                'first_50_customers': milestone_50_customers,
                'first_100_customers': milestone_100_customers,
                'break_even_month': milestone_break_even
            }
        }


# Create singleton instance for import
roi_calc = ROICalculator()
