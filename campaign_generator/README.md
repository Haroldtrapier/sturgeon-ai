# Campaign Generator

The Campaign Generator module provides AI-powered LinkedIn outreach campaign generation with personalized multi-message sequences, targeting criteria, and performance metrics.

## Features

- **5-Message Sequences**: Automatically generates a complete 5-message LinkedIn outreach sequence
- **Persona-Based Targeting**: Predefined targeting criteria for different professional personas
- **Performance Metrics**: Calculates expected campaign performance and ROI
- **Personalization Support**: Includes personalization fields for dynamic message customization

## Installation

The module is part of the Sturgeon AI platform and requires Python 3.8+.

```bash
# No additional dependencies required - uses Python standard library
```

## Usage

### Basic Usage

```python
from campaign_generator import campaign_gen

# Generate a LinkedIn outreach campaign
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    target_count=100
)
# Returns 5-message sequence + targeting + metrics
```

### Response Structure

The function returns a dictionary with the following structure:

```python
{
    "messages": [
        {
            "sequence_number": 1,
            "subject": "...",
            "body": "...",
            "delay_days": 0,
            "personalization_fields": ["{first_name}", "{company}", ...]
        },
        # ... 4 more messages
    ],
    "targeting": {
        "persona": "bd_director",
        "persona_title": "Business Development Director",
        "job_titles": [...],
        "industries": [...],
        "seniority_levels": [...],
        "company_sizes": [...],
        "locations": [...],
        "interests": [...],
        "estimated_audience_size": "50,000-100,000",
        "target_count": 100
    },
    "metrics": {
        "target_count": 100,
        "expected_connection_accepts": 25,
        "expected_message_opens": 15,
        "expected_responses": 2,
        "expected_demo_bookings": 0,
        "estimated_conversion_rates": {...},
        "estimated_roi": {...}
    },
    "campaign_summary": {
        "campaign_type": "LinkedIn Outreach",
        "target_persona": "bd_director",
        "message_sequence_length": 5,
        "total_campaign_duration_days": 12,
        "sender": "Alex from Sturgeon AI",
        "created_at": "2025-12-08T18:00:00.000000+00:00",
        "status": "ready",
        "estimated_completion_date": "2025-12-20"
    }
}
```

## Supported Personas

The module supports the following target personas:

### 1. `bd_director` - Business Development Director
Targets senior business development professionals in government contracting and professional services.

**Example:**
```python
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    target_count=100
)
```

### 2. `procurement_officer` - Procurement Officer
Targets procurement and contracting professionals in government and federal agencies.

**Example:**
```python
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="procurement_officer",
    target_count=50
)
```

### 3. `grant_manager` - Grant Manager
Targets grant managers and administrators in nonprofits, education, and research organizations.

**Example:**
```python
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="grant_manager",
    target_count=75
)
```

## Advanced Usage

### Custom Sender Name

```python
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    target_count=100,
    sender_name="John Smith from Sturgeon AI"
)
```

### Accessing Specific Data

```python
campaign = campaign_gen.generate_linkedin_outreach_campaign(
    target_persona="bd_director",
    target_count=100
)

# Access messages
for message in campaign["messages"]:
    print(f"Message {message['sequence_number']}: {message['subject']}")
    print(f"Send on Day {message['delay_days']}")

# Access targeting criteria
print(f"Job Titles: {', '.join(campaign['targeting']['job_titles'])}")
print(f"Industries: {', '.join(campaign['targeting']['industries'])}")

# Access metrics
metrics = campaign["metrics"]
print(f"Expected Responses: {metrics['expected_responses']}")
print(f"Expected ROI: ${metrics['estimated_roi']['expected_pipeline_value']:,.0f}")
```

## Message Sequence

Each campaign generates a 5-message sequence spaced 3 days apart:

1. **Day 0**: Introduction and value proposition
2. **Day 3**: Follow-up with specific example/case study
3. **Day 6**: Feature overview and benefits
4. **Day 9**: Case study with concrete results
5. **Day 12**: Final follow-up with trial offer

## Personalization

Messages include personalization fields that should be replaced with actual values:

- `{first_name}`: Target's first name
- `{company}`: Target's company name
- `{sender_name}`: Sender's name
- `{similar_company}`: Similar company for social proof

## Metrics Calculation

The module calculates expected campaign performance based on industry benchmarks:

- **Connection Accept Rate**: 25%
- **Message Open Rate**: 60%
- **Response Rate**: 8%
- **Demo Booking Rate**: 15% of responses

## Error Handling

The function raises `ValueError` in the following cases:

```python
# Invalid persona
try:
    campaign_gen.generate_linkedin_outreach_campaign(
        target_persona="invalid_persona",
        target_count=100
    )
except ValueError as e:
    print(f"Error: {e}")
    # Error: Unknown target_persona: 'invalid_persona'. Available personas: ...

# Invalid target count
try:
    campaign_gen.generate_linkedin_outreach_campaign(
        target_persona="bd_director",
        target_count=-10
    )
except ValueError as e:
    print(f"Error: {e}")
    # Error: target_count must be positive, got: -10
```

## Testing

Run the test suite:

```bash
pytest campaign_generator/test_campaign_gen.py -v
```

## License

Part of Sturgeon AI - Government Contracting & Grants Intelligence Platform
