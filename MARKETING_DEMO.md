# Marketing Director Demo

This directory contains the Sturgeon AI Marketing Director demo, which showcases marketing campaign generation and ROI calculation capabilities.

## Files

- **marketing_director_demo.py** - Interactive demo script with menu interface
- **campaign_generator.py** - Campaign generation module (LinkedIn, Email sequences)
- **roi_calculator.py** - ROI calculation and budget optimization module

## Usage

### Running the Interactive Demo

```bash
python3 marketing_director_demo.py
```

The interactive menu will present 5 demo options:

1. **LinkedIn Outreach Campaign** - Generate a complete 5-message LinkedIn outreach sequence
2. **Email Nurture Sequence** - Generate a 7-email drip campaign for free-to-paid conversion
3. **ROI Calculator** - Calculate expected ROI for marketing campaigns
4. **Budget Optimization** - Optimize budget allocation across multiple channels
5. **Growth Projection** - Project 12-month growth trajectory with marketing spend

### Using Modules Programmatically

```python
from campaign_generator import campaign_gen
from roi_calculator import roi_calc

# Generate LinkedIn campaign
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    campaign_goal="demo_bookings",
    target_count=100
)

# Calculate ROI
roi = roi_calc.calculate_campaign_roi(
    channel="linkedin_ads",
    budget=5000,
    duration_months=3
)

# Optimize budget allocation
allocation = roi_calc.optimize_budget_allocation(
    total_budget=10000,
    channels=["linkedin_ads", "content_marketing", "email_marketing"]
)

# Project growth
projection = roi_calc.project_growth_trajectory(
    monthly_budget=3000,
    duration_months=12
)
```

## Features

### Campaign Generator
- **LinkedIn Outreach Campaigns**: Ready-to-use message sequences with targeting criteria
- **Email Nurture Sequences**: Multi-email drip campaigns with subject lines and full content
- **Success Metrics**: Built-in benchmarks and KPI tracking
- **Execution Checklists**: Step-by-step implementation guides

### ROI Calculator
- **Campaign ROI Analysis**: Calculate expected returns for different marketing channels
- **Multi-Channel Optimization**: Optimize budget allocation across channels
- **Growth Projections**: Project 12-month customer and revenue growth
- **Efficiency Metrics**: CAC, LTV, payback period, and more

## Supported Marketing Channels

- LinkedIn Ads
- Content Marketing
- Email Marketing
- Google Ads
- SEO

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Internal Use

This demo is for internal use only by Trapier Management LLC.
