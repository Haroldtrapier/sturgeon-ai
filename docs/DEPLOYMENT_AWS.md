# Deploying Sturgeon AI to AWS

## Architecture

- **EC2/ECS**: Application servers
- **RDS**: PostgreSQL database
- **S3**: Static assets
- **CloudFront**: CDH

## Quick Start

```bash
# 1. Create RDS
aws rds create-db-instance --db-instance-identifier sturgeon-ai-db
```

## Cost: ~$40-60/month