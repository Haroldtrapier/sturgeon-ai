"""
STURGEON AI MARKETING DIRECTOR - ROI CALCULATOR
Calculate marketing campaign ROI and optimize spend
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class CampaignMetrics:
    """Campaign performance metrics"""
    spend: float
    impressions: int
    clicks: int
    leads: int
    demos: int
    customers: int
    revenue: float


class ROICalculator:
    """Calculate and optimize marketing ROI"""
    
    # Conversion rate constants
    DEMO_BOOKING_RATE = 0.30  # 30% of leads book demos
    DEMO_CONVERSION_RATE = 0.25  # 25% of demos convert to customers
    CUSTOMER_LIFETIME_YEARS = 2.5  # Average customer lifetime in years
    MONTHLY_SUBSCRIPTION_PRICE = 199  # Monthly subscription price in USD
    
    def __init__(self):
        # Industry benchmarks
        self.benchmarks = {
            "linkedin_ads": {
                "cpc": 5.50,
                "ctr": 0.025,
                "conversion_rate": 0.05,
                "avg_deal_size": 2388  # Annual contract value
            },
            "google_ads": {
                "cpc": 3.75,
                "ctr": 0.035,
                "conversion_rate": 0.08,
                "avg_deal_size": 2388
            },
            "content_marketing": {
                "cost_per_article": 500,
                "traffic_per_article": 1000,
                "conversion_rate": 0.02,
                "avg_deal_size": 2388
            },
            "email_marketing": {
                "cost_per_send": 0.01,
                "open_rate": 0.25,
                "click_rate": 0.05,
                "conversion_rate": 0.08,
                "avg_deal_size": 2388
            }
        }
    
    def calculate_campaign_roi(
        self,
        channel: str,
        budget: float,
        duration_months: int = 3
    ) -> Dict[str, Any]:
        """
        Calculate expected ROI for a marketing campaign
        
        Args:
            channel: Marketing channel (linkedin_ads, google_ads, etc.)
            budget: Total budget allocation
            duration_months: Campaign duration
            
        Returns:
            Complete ROI analysis with projections
        """
        
        if channel not in self.benchmarks:
            return {"error": f"Unknown channel: {channel}"}
        
        bench = self.benchmarks[channel]
        
        if "cpc" in bench:
            # Paid advertising channels
            clicks = int(budget / bench["cpc"])
            leads = int(clicks * bench["conversion_rate"])
            demos = int(leads * self.DEMO_BOOKING_RATE)
            customers = int(demos * self.DEMO_CONVERSION_RATE)
            revenue = customers * bench["avg_deal_size"]
            
        elif channel == "content_marketing":
            # Content marketing
            articles = int(budget / bench["cost_per_article"])
            traffic = articles * bench["traffic_per_article"]
            leads = int(traffic * bench["conversion_rate"])
            demos = int(leads * self.DEMO_BOOKING_RATE)
            customers = int(demos * self.DEMO_CONVERSION_RATE)
            revenue = customers * bench["avg_deal_size"]
            clicks = traffic
            
        elif channel == "email_marketing":
            # Email campaigns
            sends = int(budget / bench["cost_per_send"])
            opens = int(sends * bench["open_rate"])
            clicks = int(opens * bench["click_rate"])
            leads = int(clicks * bench["conversion_rate"])
            demos = int(leads * self.DEMO_BOOKING_RATE)
            customers = int(demos * self.DEMO_CONVERSION_RATE)
            revenue = customers * bench["avg_deal_size"]
        
        # Calculate ROI metrics
        cac = budget / customers if customers > 0 else 0
        ltv = bench["avg_deal_size"] * self.CUSTOMER_LIFETIME_YEARS
        roi = ((revenue - budget) / budget * 100) if budget > 0 else 0
        roas = revenue / budget if budget > 0 else 0
        payback_months = cac / (bench["avg_deal_size"] / 12) if customers > 0 else 0
        
        return {
            "channel": channel,
            "investment": {
                "budget": budget,
                "duration_months": duration_months,
                "monthly_spend": budget / duration_months
            },
            "performance": {
                "clicks": clicks,
                "leads": leads,
                "demos_booked": demos,
                "customers_acquired": customers,
                "revenue_generated": revenue
            },
            "efficiency_metrics": {
                "cac": round(cac, 2),
                "ltv": round(ltv, 2),
                "ltv_cac_ratio": round(ltv / cac, 2) if cac > 0 else 0,
                "payback_period_months": round(payback_months, 1)
            },
            "returns": {
                "roi_percentage": round(roi, 1),
                "roas": round(roas, 2),
                "profit": revenue - budget,
                "break_even_customers": int(budget / bench["avg_deal_size"])
            },
            "projections": {
                "month_1_revenue": revenue * 0.15,
                "month_2_revenue": revenue * 0.30,
                "month_3_revenue": revenue * 0.55,
                "annual_revenue_run_rate": revenue * 4
            },
            "recommendation": self._generate_recommendation(roi, ltv/cac if cac > 0 else 0)
        }
    
    def optimize_budget_allocation(
        self,
        total_budget: float,
        channels: List[str]
    ) -> Dict[str, Any]:
        """
        Optimize budget allocation across multiple channels
        
        Args:
            total_budget: Total marketing budget
            channels: List of channels to allocate to
            
        Returns:
            Optimized allocation strategy
        """
        
        # Calculate ROI for each channel with equal allocation
        equal_allocation = total_budget / len(channels)
        channel_performance = {}
        
        for channel in channels:
            if channel in self.benchmarks:
                analysis = self.calculate_campaign_roi(channel, equal_allocation)
                channel_performance[channel] = {
                    "roi": analysis["returns"]["roi_percentage"],
                    "customers": analysis["performance"]["customers_acquired"],
                    "revenue": analysis["performance"]["revenue_generated"]
                }
        
        # Rank channels by ROI
        ranked_channels = sorted(
            channel_performance.items(),
            key=lambda x: x[1]["roi"],
            reverse=True
        )
        
        # Allocate budget (60% to top performer, 30% to second, 10% to third)
        allocations = {}
        if len(ranked_channels) >= 3:
            allocations[ranked_channels[0][0]] = total_budget * 0.60
            allocations[ranked_channels[1][0]] = total_budget * 0.30
            allocations[ranked_channels[2][0]] = total_budget * 0.10
        elif len(ranked_channels) == 2:
            allocations[ranked_channels[0][0]] = total_budget * 0.70
            allocations[ranked_channels[1][0]] = total_budget * 0.30
        else:
            allocations[ranked_channels[0][0]] = total_budget
        
        # Calculate total expected performance
        total_customers = 0
        total_revenue = 0
        
        detailed_allocations = {}
        for channel, allocation in allocations.items():
            analysis = self.calculate_campaign_roi(channel, allocation)
            total_customers += analysis["performance"]["customers_acquired"]
            total_revenue += analysis["performance"]["revenue_generated"]
            detailed_allocations[channel] = {
                "budget": allocation,
                "percentage": round(allocation / total_budget * 100, 1),
                "expected_customers": analysis["performance"]["customers_acquired"],
                "expected_revenue": analysis["performance"]["revenue_generated"],
                "roi": analysis["returns"]["roi_percentage"]
            }
        
        # Build execution priority list based on number of channels
        execution_priority = [
            f"1. Launch {ranked_channels[0][0]} with ${allocations[ranked_channels[0][0]]:,.0f} (highest ROI)"
        ]
        if len(ranked_channels) >= 2:
            execution_priority.append(
                f"2. Add {ranked_channels[1][0]} with ${allocations[ranked_channels[1][0]]:,.0f} after 30 days"
            )
        if len(ranked_channels) >= 3:
            execution_priority.append(
                f"3. Test {ranked_channels[2][0]} with ${allocations[ranked_channels[2][0]]:,.0f} after 60 days"
            )
        
        return {
            "total_budget": total_budget,
            "optimized_allocation": detailed_allocations,
            "channel_ranking": [ch[0] for ch in ranked_channels],
            "total_expected_results": {
                "customers": total_customers,
                "revenue": total_revenue,
                "roi": round((total_revenue - total_budget) / total_budget * 100, 1),
                "average_cac": round(total_budget / total_customers, 2) if total_customers > 0 else 0
            },
            "execution_priority": execution_priority
        }
    
    def _generate_recommendation(self, roi: float, ltv_cac_ratio: float) -> str:
        """Generate strategic recommendation based on metrics"""
        
        if roi > 200 and ltv_cac_ratio > 3:
            return "SCALE AGGRESSIVELY: Outstanding performance. Increase budget by 2-3x."
        elif roi > 100 and ltv_cac_ratio > 2:
            return "SCALE: Strong performance. Increase budget by 50-100%."
        elif roi > 50 and ltv_cac_ratio > 1.5:
            return "OPTIMIZE & SCALE: Good performance. Improve conversion rates, then scale."
        elif roi > 0 and ltv_cac_ratio > 1:
            return "OPTIMIZE: Profitable but suboptimal. Test new creative and audiences."
        else:
            return "PAUSE & PIVOT: Underperforming. Revise strategy or reallocate budget."
    
    def project_growth_trajectory(
        self,
        monthly_budget: float,
        duration_months: int = 12,
        channel_mix: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Project 12-month growth trajectory
        
        Args:
            monthly_budget: Monthly marketing budget
            duration_months: Projection period
            channel_mix: Budget allocation by channel (percentages)
        """
        
        if not channel_mix:
            channel_mix = {
                "linkedin_ads": 0.40,
                "content_marketing": 0.30,
                "email_marketing": 0.20,
                "google_ads": 0.10
            }
        
        monthly_projections = []
        cumulative_customers = 0
        cumulative_revenue = 0
        
        for month in range(1, duration_months + 1):
            month_results = {
                "month": month,
                "budget": monthly_budget,
                "customers": 0,
                "revenue": 0,
                "mrr": 0
            }
            
            # Calculate results per channel
            for channel, percentage in channel_mix.items():
                channel_budget = monthly_budget * percentage
                analysis = self.calculate_campaign_roi(channel, channel_budget, 1)
                month_results["customers"] += analysis["performance"]["customers_acquired"]
                month_results["revenue"] += analysis["performance"]["revenue_generated"]
            
            # Add compound effect (previous customers still paying)
            month_results["mrr"] = (cumulative_customers + month_results["customers"]) * self.MONTHLY_SUBSCRIPTION_PRICE
            cumulative_customers += month_results["customers"]
            cumulative_revenue += month_results["revenue"]
            
            month_results["cumulative_customers"] = cumulative_customers
            month_results["cumulative_revenue"] = cumulative_revenue
            
            monthly_projections.append(month_results)
        
        return {
            "projection_period": f"{duration_months} months",
            "monthly_budget": monthly_budget,
            "total_investment": monthly_budget * duration_months,
            "channel_allocation": channel_mix,
            "monthly_breakdown": monthly_projections,
            "year_end_totals": {
                "total_customers": cumulative_customers,
                "total_revenue": cumulative_revenue,
                "final_mrr": monthly_projections[-1]["mrr"],
                "total_roi": round((cumulative_revenue - (monthly_budget * duration_months)) / (monthly_budget * duration_months) * 100, 1)
            },
            "key_milestones": {
                "break_even_month": self._find_break_even_month(monthly_projections, monthly_budget),
                "1000_customers_month": self._find_milestone_month(monthly_projections, 1000),
                "100k_mrr_month": self._find_mrr_milestone_month(monthly_projections, 100000)
            }
        }
    
    def _find_break_even_month(self, projections: List[Dict], monthly_budget: float) -> int:
        """Find the month when cumulative revenue exceeds cumulative spend"""
        for proj in projections:
            if proj["cumulative_revenue"] >= (monthly_budget * proj["month"]):
                return proj["month"]
        return -1
    
    def _find_milestone_month(self, projections: List[Dict], target_customers: int) -> int:
        """Find month when customer milestone is reached"""
        for proj in projections:
            if proj["cumulative_customers"] >= target_customers:
                return proj["month"]
        return -1
    
    def _find_mrr_milestone_month(self, projections: List[Dict], target_mrr: float) -> int:
        """Find month when MRR milestone is reached"""
        for proj in projections:
            if proj["mrr"] >= target_mrr:
                return proj["month"]
        return -1


# Instantiate for use
roi_calc = ROICalculator()
