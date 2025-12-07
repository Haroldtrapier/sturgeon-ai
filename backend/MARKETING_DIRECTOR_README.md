# Marketing Director Demo

An interactive demo system showcasing AI-powered marketing campaign generation, ROI calculation, and growth projection capabilities for Sturgeon AI.

## Overview

This demo provides marketing intelligence tools specifically designed for government contracting and B2B SaaS businesses. It includes:

- **Campaign Generation**: Pre-built LinkedIn outreach and email nurture sequences
- **ROI Analysis**: Multi-channel marketing ROI calculations with industry benchmarks
- **Budget Optimization**: Intelligent budget allocation across marketing channels
- **Growth Projections**: 12-month revenue and customer acquisition forecasts

## Files

- `marketing_director_demo.py` - Interactive demo interface
- `campaign_generator.py` - Campaign template generation engine
- `roi_calculator.py` - ROI calculation and optimization engine

## Usage

### Running the Demo

```bash
cd backend
python3 marketing_director_demo.py
```

The interactive menu will present 5 demo options:

1. **LinkedIn Outreach Campaign** - Generate a 5-message LinkedIn sequence for BD Directors
2. **Email Nurture Sequence** - Create a 7-email free-to-paid conversion sequence
3. **ROI Calculator** - Calculate expected ROI for a $5,000 LinkedIn Ads campaign
4. **Budget Optimization** - Optimize $10,000 across multiple marketing channels
5. **Growth Projection** - Project 12-month growth with $3,000/month budget

### Using the Modules Programmatically

#### Campaign Generator

```python
from campaign_generator import campaign_gen

# Generate LinkedIn campaign
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    campaign_goal="demo_bookings",
    target_count=100
)

# Generate email sequence
sequence = campaign_gen.generate_email_nurture_sequence(
    segment="free_users",
    goal="upgrade_to_paid"
)
```

#### ROI Calculator

```python
from roi_calculator import roi_calc

# Calculate campaign ROI
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

# Project growth trajectory
projection = roi_calc.project_growth_trajectory(
    monthly_budget=3000,
    duration_months=12
)
```

## Supported Marketing Channels

The ROI calculator includes benchmarks for:

- **LinkedIn Ads** - Highest ROI for B2B, best for targeting specific job titles
- **Content Marketing** - Blog posts, whitepapers, case studies
- **Email Marketing** - Newsletter campaigns, drip sequences
- **Google Ads** - Search and display advertising

## Configuration

Key parameters can be adjusted in the class constants:

### Campaign Generator (`campaign_generator.py`)
```python
DEMO_BOOKING_RATE = 0.08  # 8% conversion rate for demo bookings
```

### ROI Calculator (`roi_calculator.py`)
```python
VIRAL_COEFFICIENT = 0.05  # 5% monthly viral growth
MONTHLY_SUBSCRIPTION_VALUE = 200  # MRR per customer
ALLOCATION_STRATEGY = [0.50, 0.30, 0.20]  # Budget split for top 3 channels
CUSTOMER_RETENTION_YEARS = 2  # Average retention period
```

## Benchmarks Used

### LinkedIn Ads
- CPM: $75
- CTR: 2.5%
- Conversion Rate: 8%
- Avg Customer Value: $2,400/year

### Content Marketing
- Cost per Article: $500
- Traffic per Article: 500 visitors
- Conversion Rate: 3%

### Email Marketing
- Cost per Send: $0.05
- Open Rate: 25%
- Click Rate: 12%
- Conversion Rate: 6%

### Google Ads
- CPC: $8.50
- Conversion Rate: 5%

## Example Output

### LinkedIn Campaign
```
Campaign Name: Government Contracting BD Directors - Demo Booking Campaign
Timeline: 21 days
Touchpoints: 5 messages
Expected Demos Booked: 8 (from 100 targets)
```

### ROI Calculator
```
Investment: $5,000 over 3 months
Expected Customers: 133
Total Revenue: $320,000
ROI: 6,300%
Payback Period: 0.2 months
```

### Budget Optimization
```
Total Budget: $10,000
Optimized Allocation:
- Content Marketing: $5,000 (50%)
- Email Marketing: $3,000 (30%)
- LinkedIn Ads: $2,000 (20%)
Total Expected Customers: 287
Blended ROI: 6,796%
```

## Notes

- All calculations are based on industry benchmarks and historical data
- Actual results may vary based on campaign execution, market conditions, and competition
- This is a demonstration tool designed for internal planning purposes
- ROI projections assume consistent execution and optimization over time

## Future Enhancements

Potential additions for future versions:

- Additional campaign personas (Sales Engineers, CISOs, etc.)
- More marketing channels (Partnerships, Events, Webinars)
- A/B test simulation and optimization
- Integration with actual marketing platforms (LinkedIn, HubSpot)
- Real-time performance tracking and adjustment
- Custom benchmark configuration per company

## Support

For questions or issues with the marketing demo tools, contact the development team or refer to the main Sturgeon AI documentation.
