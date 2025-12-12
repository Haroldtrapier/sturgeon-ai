#!/usr/bin/env python3
"""
ROI Calculator Module for Sturgeon AI Marketing Director
Calculates marketing ROI, optimizes budget allocation, and projects growth
"""


class ROICalculator:
    """Calculate marketing ROI and optimize budget allocation"""
    
    def __init__(self):
        # Channel-specific performance metrics
        self.channel_metrics = {
            "linkedin_ads": {
                "cpm": 35,  # Cost per 1000 impressions
                "ctr": 0.025,  # Click-through rate
                "conversion_rate": 0.08,  # Lead to customer
                "avg_customer_value": 1200,  # Annual contract value
                "sales_cycle_days": 45
            },
            "content_marketing": {
                "cost_per_piece": 500,
                "pieces_per_month": 8,
                "visitors_per_piece": 200,
                "conversion_rate": 0.05,
                "avg_customer_value": 1200,
                "sales_cycle_days": 60
            },
            "email_marketing": {
                "cost_per_send": 0.05,
                "sends_per_month": 10000,
                "open_rate": 0.28,
                "ctr": 0.12,
                "conversion_rate": 0.06,
                "avg_customer_value": 1200,
                "sales_cycle_days": 30
            },
            "google_ads": {
                "cpc": 12,  # Cost per click
                "clicks_per_1000": 50,
                "conversion_rate": 0.05,
                "avg_customer_value": 1200,
                "sales_cycle_days": 35
            }
        }
    
    def calculate_campaign_roi(self, channel, budget, duration_months):
        """
        Calculate expected ROI for a marketing campaign
        
        Args:
            channel: Marketing channel (e.g., "linkedin_ads")
            budget: Total budget for campaign
            duration_months: Campaign duration in months
            
        Returns:
            dict: Complete ROI analysis with metrics
        """
        if channel not in self.channel_metrics:
            raise ValueError(f"Unknown channel: {channel}. Available: {list(self.channel_metrics.keys())}")
        
        metrics = self.channel_metrics[channel]
        monthly_spend = budget / duration_months
        
        # Calculate channel-specific performance
        if channel == "linkedin_ads":
            impressions = (budget / metrics["cpm"]) * 1000
            clicks = impressions * metrics["ctr"]
            leads = clicks * metrics["conversion_rate"]
            customers = leads
        elif channel == "content_marketing":
            pieces = metrics["pieces_per_month"] * duration_months
            visitors = pieces * metrics["visitors_per_piece"]
            leads = visitors * metrics["conversion_rate"]
            customers = leads
        elif channel == "email_marketing":
            sends = metrics["sends_per_month"] * duration_months
            opens = sends * metrics["open_rate"]
            clicks = opens * metrics["ctr"]
            leads = clicks * metrics["conversion_rate"]
            customers = leads
        else:  # google_ads
            clicks = (budget / metrics["cpc"])
            leads = clicks * metrics["conversion_rate"]
            customers = leads
        
        # Calculate financial metrics
        revenue = customers * metrics["avg_customer_value"]
        profit = revenue - budget
        roi_percentage = (profit / budget) * 100 if budget > 0 else 0
        roi_multiple = revenue / budget if budget > 0 else 0
        
        # Calculate efficiency metrics
        cost_per_customer = budget / customers if customers > 0 else 0
        customer_ltv = metrics["avg_customer_value"] * 3  # Assume 3-year retention
        ltv_to_cac_ratio = customer_ltv / cost_per_customer if cost_per_customer > 0 else 0
        payback_months = cost_per_customer / (metrics["avg_customer_value"] / 12) if metrics["avg_customer_value"] > 0 else 0
        
        result = {
            "channel": channel,
            "investment": {
                "budget": budget,
                "duration_months": duration_months,
                "monthly_spend": monthly_spend
            },
            "performance": {
                "leads": int(leads),
                "customers": int(customers),
                "revenue": revenue,
                "profit": profit
            },
            "efficiency_metrics": {
                "cost_per_customer": cost_per_customer,
                "customer_ltv": customer_ltv,
                "ltv_to_cac_ratio": ltv_to_cac_ratio,
                "payback_months": payback_months
            },
            "returns": {
                "roi_percentage": roi_percentage,
                "roi_multiple": roi_multiple,
                "profit": profit,
                "revenue": revenue
            },
            "recommendation": self._generate_recommendation(roi_percentage, ltv_to_cac_ratio, channel)
        }
        
        return result
    
    def _generate_recommendation(self, roi_percentage, ltv_cac_ratio, channel):
        """Generate strategic recommendation based on metrics"""
        if roi_percentage > 300 and ltv_cac_ratio > 3:
            return f"EXCELLENT: Strong ROI and healthy unit economics. Scale {channel} investment aggressively."
        elif roi_percentage > 200 and ltv_cac_ratio > 2:
            return f"GOOD: Positive returns with room to scale. Consider increasing {channel} budget by 50%."
        elif roi_percentage > 100 and ltv_cac_ratio > 1.5:
            return f"MODERATE: Profitable but watch efficiency. Optimize {channel} before scaling further."
        elif roi_percentage > 0:
            return f"MARGINAL: Breaking even. Test and optimize {channel} campaigns before additional investment."
        else:
            return f"POOR: Negative ROI. Pause {channel} and investigate issues before continuing."
    
    def optimize_budget_allocation(self, total_budget, channels):
        """
        Optimize budget allocation across multiple channels
        
        Args:
            total_budget: Total marketing budget to allocate
            channels: List of channels to include
            
        Returns:
            dict: Optimized allocation with expected results
        """
        # Validate inputs
        if not channels:
            raise ValueError("At least one channel must be provided")
        if len(channels) < 2:
            raise ValueError("At least two channels must be provided for optimization")
        
        # Calculate ROI for each channel with equal split
        test_budget = total_budget / len(channels)
        channel_performance = {}
        
        for channel in channels:
            roi_data = self.calculate_campaign_roi(channel, test_budget, 3)
            channel_performance[channel] = {
                "roi_multiple": roi_data["returns"]["roi_multiple"],
                "customers": roi_data["performance"]["customers"],
                "ltv_cac_ratio": roi_data["efficiency_metrics"]["ltv_to_cac_ratio"]
            }
        
        # Sort channels by ROI multiple
        sorted_channels = sorted(
            channel_performance.items(),
            key=lambda x: x[1]["roi_multiple"],
            reverse=True
        )
        
        # Allocate budget based on ROI (weighted approach)
        total_roi = sum(perf["roi_multiple"] for _, perf in sorted_channels)
        
        # Handle edge case where all channels have zero ROI
        if total_roi == 0:
            # Fall back to equal distribution
            total_roi = len(sorted_channels)
            for _, perf in sorted_channels:
                perf["roi_multiple"] = 1.0
        
        allocation = {}
        
        for channel, perf in sorted_channels:
            weight = perf["roi_multiple"] / total_roi
            channel_budget = total_budget * weight
            
            # Calculate expected results with optimized budget
            roi_data = self.calculate_campaign_roi(channel, channel_budget, 3)
            
            allocation[channel] = {
                "budget": channel_budget,
                "percentage": int(weight * 100),
                "expected_customers": roi_data["performance"]["customers"],
                "expected_revenue": roi_data["performance"]["revenue"],
                "roi": roi_data["returns"]["roi_percentage"]
            }
        
        # Calculate total expected results
        total_customers = sum(ch["expected_customers"] for ch in allocation.values())
        total_revenue = sum(ch["expected_revenue"] for ch in allocation.values())
        total_roi = ((total_revenue - total_budget) / total_budget) * 100
        
        result = {
            "total_budget": total_budget,
            "optimized_allocation": allocation,
            "total_expected_results": {
                "total_customers": total_customers,
                "total_revenue": total_revenue,
                "blended_roi": total_roi,
                "profit": total_revenue - total_budget
            },
            "execution_priority": [
                f"1. Start with {sorted_channels[0][0].replace('_', ' ').title()} (highest ROI: {sorted_channels[0][1]['roi_multiple']:.1f}x)",
                f"2. Layer in {sorted_channels[1][0].replace('_', ' ').title()} after 30 days" if len(sorted_channels) > 1 else None,
                f"3. Add {sorted_channels[2][0].replace('_', ' ').title()} once first two channels are optimized" if len(sorted_channels) > 2 else None,
                "4. Review and rebalance monthly based on actual performance"
            ]
        }
        
        return result
    
    def project_growth_trajectory(self, monthly_budget, duration_months):
        """
        Project growth trajectory over time
        
        Args:
            monthly_budget: Monthly marketing budget
            duration_months: Projection period in months
            
        Returns:
            dict: Month-by-month growth projection
        """
        # Allocate budget across channels (typical mix)
        allocation = {
            "linkedin_ads": 0.35,
            "content_marketing": 0.30,
            "email_marketing": 0.25,
            "google_ads": 0.10
        }
        
        monthly_breakdown = []
        cumulative_customers = 0
        cumulative_revenue = 0
        
        for month in range(duration_months):
            month_customers = 0
            month_revenue = 0
            
            # Calculate results for each channel
            for channel, percentage in allocation.items():
                channel_budget = monthly_budget * percentage
                
                # Account for improvement over time (learning curve)
                efficiency_multiplier = min(1.0 + (month * 0.05), 1.5)  # Up to 50% improvement
                
                roi_data = self.calculate_campaign_roi(channel, channel_budget, 1)
                channel_customers = roi_data["performance"]["customers"] * efficiency_multiplier
                channel_revenue = roi_data["performance"]["revenue"] * efficiency_multiplier
                
                month_customers += channel_customers
                month_revenue += channel_revenue
            
            cumulative_customers += month_customers
            # Account for MRR growth (existing + new customers)
            monthly_recurring = cumulative_customers * 100  # $100 MRR per customer
            cumulative_revenue += month_revenue
            
            monthly_breakdown.append({
                "month": month + 1,
                "spend": monthly_budget,
                "customers": int(month_customers),
                "cumulative_customers": int(cumulative_customers),
                "mrr": monthly_recurring,
                "monthly_revenue": month_revenue,
                "cumulative_revenue": cumulative_revenue
            })
        
        # Calculate year-end totals
        total_investment = monthly_budget * duration_months
        final_month = monthly_breakdown[-1]
        
        result = {
            "monthly_budget": monthly_budget,
            "projection_period": f"{duration_months} months",
            "total_investment": total_investment,
            "channel_allocation": allocation,
            "monthly_breakdown": monthly_breakdown,
            "year_end_totals": {
                "total_customers": final_month["cumulative_customers"],
                "annual_revenue": final_month["cumulative_revenue"],
                "mrr": final_month["mrr"],
                "arr": final_month["mrr"] * 12,
                "roi": ((final_month["cumulative_revenue"] - total_investment) / total_investment) * 100
            },
            "key_milestones": {
                "breakeven_month": self._find_breakeven_month(monthly_breakdown, total_investment),
                "100_customers_month": self._find_milestone_month(monthly_breakdown, "cumulative_customers", 100),
                "10k_mrr_month": self._find_milestone_month(monthly_breakdown, "mrr", 10000),
                "positive_roi_month": self._find_positive_roi_month(monthly_breakdown, monthly_budget)
            }
        }
        
        return result
    
    def _find_breakeven_month(self, breakdown, total_investment):
        """Find month when cumulative revenue exceeds investment"""
        cumulative_spend = 0
        for month_data in breakdown:
            cumulative_spend += month_data["spend"]
            if month_data["cumulative_revenue"] >= cumulative_spend:
                return month_data["month"]
        return 0  # Not achieved
    
    def _find_milestone_month(self, breakdown, metric, threshold):
        """Find month when metric exceeds threshold"""
        for month_data in breakdown:
            if month_data[metric] >= threshold:
                return month_data["month"]
        return 0  # Not achieved
    
    def _find_positive_roi_month(self, breakdown, monthly_budget):
        """Find month when ROI becomes positive"""
        cumulative_spend = 0
        for month_data in breakdown:
            cumulative_spend += monthly_budget
            month_roi = ((month_data["cumulative_revenue"] - cumulative_spend) / cumulative_spend) * 100
            if month_roi > 0:
                return month_data["month"]
        return 0  # Not achieved


# Create singleton instance
roi_calc = ROICalculator()
