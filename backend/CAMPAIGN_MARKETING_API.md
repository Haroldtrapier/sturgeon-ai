# LinkedIn Campaign Generator & ROI Calculator API

This document describes the campaign generation and ROI calculation APIs for Sturgeon AI.

## Overview

Two new modules provide marketing campaign management capabilities:
- **campaign_generator**: Creates LinkedIn outreach campaigns with message sequences
- **roi_calculator**: Calculates ROI and optimizes budget allocation

## Installation

Dependencies are already included in `requirements.txt`. If needed:

```bash
cd backend
pip install -r requirements.txt
```

## Quick Start

### Generate LinkedIn Campaign

Create a complete 5-message LinkedIn outreach campaign:

```python
from campaign_generator import campaign_gen

campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    target_count=100
)
```

**Returns:**
- Complete 5-message sequence with timing
- Targeting criteria (job titles, industries, company size, seniority)
- Expected performance metrics (connection, response, meeting, conversion rates)
- Campaign ID and metadata

**Available Personas:**
- `bd_director` - Business Development Directors
- `sales_manager` - Sales Managers
- `marketing_director` - Marketing Directors

### Calculate Campaign ROI

Calculate expected ROI for a marketing campaign:

```python
from roi_calculator import roi_calc

roi = roi_calc.calculate_campaign_roi("linkedin_ads", 5000)
```

**Returns:**
```python
{
    'campaign_type': 'linkedin_ads',
    'budget': 5000.0,
    'expected_customers': 18,
    'expected_revenue': 42984.0,
    'roi_percentage': 759.7,
    'cost_per_customer': 277.78,
    'customer_lifetime_value': 2388.0
}
```

**Supported Channels:**
- `linkedin_ads` - LinkedIn advertising
- `content_marketing` - Content marketing campaigns
- `email_marketing` - Email outreach
- `google_ads` - Google advertising
- `linkedin_outreach` - Direct LinkedIn outreach
- `webinars` - Webinar campaigns

### Optimize Budget Allocation

Get optimal budget distribution across channels:

```python
from roi_calculator import roi_calc

allocation = roi_calc.optimize_budget_allocation(
    10000, 
    ["linkedin_ads", "content_marketing", "email_marketing"]
)
```

**Returns:**
- Optimal 60/30/10 split (or appropriate split for channel count)
- Per-channel budget, expected customers, revenue, and ROI
- Blended ROI across all channels
- Total expected customers and revenue

## API Reference

### CampaignGenerator

#### `generate_linkedin_outreach_campaign(target_persona, target_count)`

Generate a complete LinkedIn outreach campaign.

**Parameters:**
- `target_persona` (str): Type of persona to target (default: "bd_director")
- `target_count` (int): Number of prospects to target (default: 100)

**Returns:** Dictionary containing:
- `campaign_id` (str): Unique campaign identifier
- `target_persona` (str): Persona type
- `target_count` (int): Number of prospects
- `messages` (list): 5-message sequence with content, timing, and type
- `targeting` (dict): Job titles, industries, company sizes, seniority levels, locations
- `metrics` (dict): Expected connection, response, meeting, and conversion rates
- `created_at` (str): ISO format timestamp

### ROICalculator

#### `calculate_campaign_roi(campaign_type, budget)`

Calculate expected ROI for a marketing campaign.

**Parameters:**
- `campaign_type` (str): Marketing channel type
- `budget` (float): Campaign budget in dollars

**Returns:** Dictionary containing:
- `campaign_type` (str): Channel type
- `budget` (float): Campaign budget
- `expected_customers` (int): Expected customer acquisitions
- `expected_revenue` (float): Expected revenue (with LTV)
- `roi_percentage` (float): ROI percentage
- `cost_per_customer` (float): Acquisition cost per customer
- `customer_lifetime_value` (float): LTV per customer

#### `optimize_budget_allocation(total_budget, channels)`

Optimize budget distribution across marketing channels.

**Parameters:**
- `total_budget` (float): Total marketing budget
- `channels` (list[str]): List of channel names to allocate across

**Returns:** Dictionary containing:
- `total_budget` (float): Total budget
- `allocations` (dict): Per-channel breakdown with budget, percentage, customers, revenue, ROI
- `total_expected_revenue` (float): Combined expected revenue
- `total_expected_customers` (int): Combined expected customers
- `blended_roi` (float): Weighted average ROI

## Examples

### Complete Campaign Workflow

```python
from campaign_generator import campaign_gen
from roi_calculator import roi_calc

# Step 1: Generate campaign
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    target_count=200
)

print(f"Campaign: {campaign['campaign_id']}")
print(f"Messages: {len(campaign['messages'])}")
print(f"Expected connection rate: {campaign['metrics']['expected_connection_rate']*100}%")

# Step 2: Calculate ROI for single channel
linkedin_roi = roi_calc.calculate_campaign_roi("linkedin_ads", 10000)
print(f"LinkedIn Ads ROI: {linkedin_roi['roi_percentage']}%")
print(f"Expected customers: {linkedin_roi['expected_customers']}")

# Step 3: Optimize multi-channel budget
budget_plan = roi_calc.optimize_budget_allocation(
    50000,
    ["linkedin_ads", "content_marketing", "email_marketing", "webinars"]
)

print(f"Total expected ROI: {budget_plan['blended_roi']}%")
for channel, details in budget_plan['allocations'].items():
    print(f"  {channel}: ${details['budget']:,.0f} ({details['percentage']}%)")
```

### Custom Persona Campaign

```python
# Generate campaigns for different personas
personas = ["bd_director", "sales_manager", "marketing_director"]

for persona in personas:
    campaign = campaign_gen.generate_linkedin_outreach_campaign(
        target_persona=persona,
        target_count=50
    )
    print(f"{persona}: {len(campaign['targeting']['job_titles'])} job titles targeted")
```

### ROI Comparison

```python
# Compare ROI across channels
channels = ["linkedin_ads", "content_marketing", "email_marketing", "google_ads"]
budget = 5000

print("ROI Comparison:")
for channel in channels:
    roi = roi_calc.calculate_campaign_roi(channel, budget)
    print(f"  {channel}: {roi['roi_percentage']}% ROI, "
          f"{roi['expected_customers']} customers")
```

## Testing

Run the test suite:

```bash
cd backend
python3 -m pytest test_campaign_modules.py -v
```

All 13 tests should pass:
- 5 campaign generator tests
- 8 ROI calculator tests

## Notes

- ROI calculations use industry-standard benchmarks for each channel
- Customer lifetime value (LTV) is factored into revenue projections
- Budget optimization uses efficiency scoring with diversification
- Message sequences include dynamic placeholders for personalization: `{first_name}`, `{company}`, `{industry}`, etc.

## Security

This code has been reviewed and scanned:
- ✅ Code review completed
- ✅ CodeQL security scan passed (0 vulnerabilities)
- ✅ No sensitive data exposure
- ✅ Input validation via Pydantic models

## Support

For issues or questions, please refer to the main Sturgeon AI documentation or open an issue in the repository.
