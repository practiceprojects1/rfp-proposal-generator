# AWS Deployment Guide

This guide covers deploying the RFP Proposal Generator to AWS using ECS Fargate with AWS Bedrock integration.

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Docker installed
- AWS Bedrock enabled in your account (for Claude model access)
- ECR permissions to push images

## Architecture

The deployment uses:
- **ECS Fargate**: Serverless container orchestration
- **Application Load Balancer**: Traffic distribution and health checks
- **AWS Bedrock**: Managed foundation model service for Claude
- **Secrets Manager**: Secure storage for API keys and credentials
- **CloudWatch**: Logging and monitoring
- **ECR**: Container registry

## Quick Deploy

### 1. Configure Environment Variables

```bash
export AWS_REGION=us-east-1
export ENVIRONMENT=production
export IMAGE_TAG=latest
```

### 2. Run Deployment Script

```bash
cd rfp-proposal-generator
./aws/deploy.sh
```

The script will:
1. Create ECR repository
2. Build and push Docker image
3. Set up secrets in AWS Secrets Manager
4. Deploy CloudFormation stack with ECS, ALB, and networking

### 3. Access the API

After deployment, the script will output the Load Balancer URL. Access the API at:

```bash
# Health check
curl http://YOUR-ALB-DNS/health

# Chat endpoint
curl -X POST http://YOUR-ALB-DNS/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Search for AI RFPs", "thread_id": "test"}'
```

## Manual Deployment Steps

### Step 1: Build and Push Docker Image

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t rfp-proposal-generator:latest .

# Tag for ECR
docker tag rfp-proposal-generator:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rfp-proposal-generator:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rfp-proposal-generator:latest
```

### Step 2: Create Secrets

```bash
# AWS Access Key
aws secretsmanager create-secret \
  --name rfp-proposal-generator/aws-access-key \
  --secret-string "YOUR_ACCESS_KEY"

# AWS Secret Key
aws secretsmanager create-secret \
  --name rfp-proposal-generator/aws-secret-key \
  --secret-string "YOUR_SECRET_KEY"

# Anthropic API Key (fallback if not using Bedrock)
aws secretsmanager create-secret \
  --name rfp-proposal-generator/anthropic-api-key \
  --secret-string "YOUR_ANTHROPIC_KEY"
```

### Step 3: Deploy CloudFormation Stack

```bash
aws cloudformation deploy \
  --template-file aws/cloudformation-template.yaml \
  --stack-name production-rfp-proposal-generator \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    VpcId=vpc-xxxxxxxx \
    SubnetIds=subnet-xxxx,subnet-yyyy \
    ContainerImage=YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rfp-proposal-generator:latest \
    Environment=production \
    UseBedrock=true \
  --region us-east-1
```

## AWS Bedrock Configuration

### Enable Bedrock Access

1. Go to AWS Console → Amazon Bedrock
2. Enable access to Claude models (Claude 3 Sonnet recommended)
3. Note the model ID: `anthropic.claude-3-sonnet-20240229-v1:0`

### IAM Permissions

The task role needs these permissions (included in CloudFormation template):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

## API Endpoints

Once deployed, the following endpoints are available:

### Health Check
```bash
GET /health
```

### Chat (Non-streaming)
```bash
POST /chat
Content-Type: application/json

{
  "message": "Search for AI software development RFPs",
  "thread_id": "session-123",
  "stream": false
}
```

### Chat (Streaming)
```bash
POST /chat/stream
Content-Type: application/json

{
  "message": "Generate a proposal",
  "thread_id": "session-123"
}
```

### Direct RFP Search
```bash
POST /rfp/search?keywords=AI&days_back=30&limit=10
```

### RFP Analysis
```bash
POST /rfp/analyze
Content-Type: application/json

{
  "title": "AI Software Development",
  "description": "...",
  "requirements": [...]
}
```

## Environment Variables

Configure these in your `.env` file or CloudFormation parameters:

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_BEDROCK` | Use AWS Bedrock for inference | `false` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key (fallback) | - |
| `PORT` | API server port | `8000` |
| `HOST` | API server host | `0.0.0.0` |

## Monitoring and Logging

### CloudWatch Logs

Logs are automatically sent to CloudWatch:
- Log Group: `/ecs/production-rfp-proposal-generator`
- Retention: 7 days

View logs:
```bash
aws logs tail /ecs/production-rfp-proposal-generator --follow
```

### CloudWatch Metrics

ECS provides default metrics:
- CPU utilization
- Memory utilization
- Network I/O
- Task count

### Health Checks

The ALB performs health checks on `/health` endpoint every 30 seconds.

## Scaling

### Auto Scaling

Add auto scaling to the CloudFormation template:

```yaml
AutoScalingTarget:
  Type: AWS::ApplicationAutoScaling::ScalableTarget
  Properties:
    MaxCapacity: 10
    MinCapacity: 2
    ResourceId: !Sub service/${ECSCluster.Name}/${ECSService.Name}
    ScalableDimension: ecs:service:DesiredCount
    ServiceNamespace: ecs
```

### Manual Scaling

```bash
aws ecs update-service \
  --cluster production-rfp-proposal-generator \
  --service production-rfp-proposal-generator \
  --desired-count 5
```

## Security Considerations

1. **IAM Roles**: Use least privilege for task roles
2. **Secrets Manager**: Never commit secrets to git
3. **VPC**: Deploy in private subnets for production
4. **HTTPS**: Enable HTTPS listener with ACM certificate
5. **Security Groups**: Restrict inbound traffic
6. **Container Security**: Run as non-root user (already configured)

## Troubleshooting

### Container Won't Start

Check logs:
```bash
aws logs tail /ecs/production-rfp-proposal-generator --follow
```

Common issues:
- Missing environment variables
- Insufficient IAM permissions
- Bedrock model not enabled

### Bedrock Access Denied

1. Verify Bedrock is enabled in your account
2. Check IAM permissions for `bedrock:InvokeModel`
3. Verify model ID is correct

### Health Check Failing

1. Check if port 8000 is exposed
2. Verify health check path is `/health`
3. Check security group rules

## Cost Optimization

- Use Graviton instances for cost savings
- Set appropriate task count for your workload
- Enable ECS capacity providers
- Use Spot instances for non-critical workloads

## Cleanup

To remove all resources:

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack \
  --stack-name production-rfp-proposal-generator

# Delete ECR repository
aws ecr delete-repository \
  --repository-name rfp-proposal-generator \
  --force

# Delete secrets
aws secretsmanager delete-secret \
  --secret-id rfp-proposal-generator/aws-access-key
aws secretsmanager delete-secret \
  --secret-id rfp-proposal-generator/aws-secret-key
aws secretsmanager delete-secret \
  --secret-id rfp-proposal-generator/anthropic-api-key
```

## Local Development with Docker

```bash
# Build image
docker build -t rfp-proposal-generator .

# Run container
docker run -p 8000:8000 \
  -e USE_BEDROCK=true \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  rfp-proposal-generator

# Test API
curl http://localhost:8000/health
```

## Support

For issues:
1. Check CloudWatch logs
2. Review ECS task events
3. Verify IAM permissions
4. Check Bedrock model access