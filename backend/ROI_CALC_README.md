# ROI Calculator Module

## Overview

The ROI Calculator module (`roi_calc.py`) provides functionality for optimizing marketing budget allocation across different channels with built-in ROI calculation and performance projection capabilities.

## Features

- **Budget Allocation Optimization**: Automatically allocate budgets across marketing channels based on predefined or custom strategies
- **Default Strategy**: 60% LinkedIn Ads, 30% Content Marketing, 10% Email Marketing
- **Custom Weights**: Support for user-defined allocation percentages
- **ROI Calculation**: Calculate return on investment for individual channels
- **Performance Projection**: Project revenue and profit based on historical ROI data

## Installation

No additional dependencies required beyond the standard Python library.

## Quick Start

### Basic Usage

```python
from roi_calc import ROICalculator

# Create an instance
roi_calc = ROICalculator()

# Optimize budget allocation
allocation = roi_calc.optimize_budget_allocation(
    total_budget=10000,
    channels=["linkedin_ads", "content_marketing", "email_marketing"]
)

# Output: {'linkedin_ads': 6000.0, 'content_marketing': 3000.0, 'email_marketing': 1000.0}
# Optimal split: 60% LinkedIn / 30% Content / 10% Email
```

### Convenience Function

```python
from roi_calc import optimize_budget_allocation

allocation = optimize_budget_allocation(
    total_budget=10000,
    channels=["linkedin_ads", "content_marketing", "email_marketing"]
)
```

### Custom Allocation Weights

```python
roi_calc = ROICalculator()

custom_weights = {
    "linkedin_ads": 0.40,
    "content_marketing": 0.35,
    "email_marketing": 0.25
}

allocation = roi_calc.optimize_budget_allocation(
    total_budget=15000,
    channels=["linkedin_ads", "content_marketing", "email_marketing"],
    custom_weights=custom_weights
)
```

### Calculate ROI

```python
roi_calc = ROICalculator()

roi_percentage = roi_calc.calculate_roi(
    channel="linkedin_ads",
    investment=5000,
    revenue=12000
)
# Output: 140.0 (140% ROI)
```

### Project Performance

```python
roi_calc = ROICalculator()

allocations = {
    "linkedin_ads": 6000,
    "content_marketing": 3000,
    "email_marketing": 1000
}

historical_roi = {
    "linkedin_ads": 150.0,       # 150% ROI
    "content_marketing": 200.0,   # 200% ROI
    "email_marketing": 100.0      # 100% ROI
}

performance = roi_calc.get_channel_performance(allocations, historical_roi)

# Returns detailed metrics for each channel:
# {
#     'linkedin_ads': {
#         'investment': 6000.0,
#         'roi_percentage': 150.0,
#         'projected_revenue': 15000.0,
#         'projected_profit': 9000.0
#     },
#     ...
# }
```

## API Reference

### ROICalculator Class

#### `__init__()`
Initialize the ROI Calculator with default allocation strategy.

#### `optimize_budget_allocation(total_budget, channels, custom_weights=None)`
Optimize budget allocation across marketing channels.

**Parameters:**
- `total_budget` (float): Total budget to allocate (must be positive)
- `channels` (List[str]): List of channel names to allocate budget to
- `custom_weights` (Optional[Dict[str, float]]): Custom allocation weights (must sum to 1.0)

**Returns:**
- Dict[str, float]: Dictionary mapping channel names to allocated budget amounts

**Raises:**
- `ValueError`: If total_budget is not positive or channels list is empty

#### `set_allocation_strategy(strategy)`
Set custom allocation strategy for future allocations.

**Parameters:**
- `strategy` (Dict[str, float]): Dictionary mapping channel names to allocation percentages (0-1)

**Raises:**
- `ValueError`: If percentages don't sum to approximately 1.0

#### `calculate_roi(channel, investment, revenue)`
Calculate ROI for a specific channel.

**Parameters:**
- `channel` (str): Channel name
- `investment` (float): Amount invested
- `revenue` (float): Revenue generated

**Returns:**
- float: ROI as a percentage

#### `get_channel_performance(allocations, historical_roi)`
Project performance based on allocations and historical ROI.

**Parameters:**
- `allocations` (Dict[str, float]): Current budget allocations per channel
- `historical_roi` (Dict[str, float]): Historical ROI percentages per channel

**Returns:**
- Dict[str, Dict[str, float]]: Dictionary with projected revenue and ROI per channel

## Default Channel Allocations

The default allocation strategy is optimized for typical B2B marketing scenarios:

| Channel | Allocation | Rationale |
|---------|-----------|-----------|
| LinkedIn Ads | 60% | High-quality B2B leads, professional targeting |
| Content Marketing | 30% | Long-term value, SEO benefits, thought leadership |
| Email Marketing | 10% | Nurturing existing relationships, cost-effective |

## Testing

Run the test suite:

```bash
cd backend
python -m pytest test_roi_calc.py -v
```

Current test coverage: 18 test cases covering:
- Basic allocation with default weights
- Different channel orderings
- Subset of channels
- Custom weights
- Error handling for invalid inputs
- ROI calculations
- Performance projections

## Examples

See `roi_calc_example.py` for comprehensive usage examples including:
1. Basic budget allocation
2. Custom allocation weights
3. ROI calculation
4. Performance projection

Run examples:
```bash
cd backend
python roi_calc_example.py
```

## Error Handling

The module includes validation for:
- Negative or zero budget values
- Empty channel lists
- Invalid allocation weights (not summing to 1.0)
- Zero investment in ROI calculations

## Notes

- All monetary values are returned as floats
- Small floating-point precision differences may occur (< 0.01)
- Unknown channels receive zero allocation unless they're the only channel
- ROI calculations return 0% for zero investment

## Version

Version: 1.0.0
Created: 2025-12-08
