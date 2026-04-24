#!/bin/bash

# AWS Deployment Script for RFP Proposal Generator
set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ENVIRONMENT=${ENVIRONMENT:-production}
ECR_REPOSITORY_NAME=rfp-proposal-generator
IMAGE_TAG=${IMAGE_TAG:-latest}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== RFP Proposal Generator AWS Deployment ===${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if user is authenticated
echo -e "${YELLOW}Checking AWS authentication...${NC}"
aws sts get-caller-identity > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}AWS authentication failed. Please run 'aws configure' first.${NC}"
    exit 1
fi
echo -e "${GREEN}AWS authentication successful${NC}"

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}AWS Account ID: $ACCOUNT_ID${NC}"

# Step 1: Create ECR Repository
echo -e "${YELLOW}Creating ECR repository...${NC}"
aws ecr describe-repositories --repository-names $ECR_REPOSITORY_NAME --region $AWS_REGION > /dev/null 2>&1 || \
    aws ecr create-repository --repository-name $ECR_REPOSITORY_NAME --region $AWS_REGION

# Step 2: Login to ECR
echo -e "${YELLOW}Logging in to ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 3: Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t $ECR_REPOSITORY_NAME:$IMAGE_TAG .

# Step 4: Tag image for ECR
echo -e "${YELLOW}Tagging image for ECR...${NC}"
docker tag $ECR_REPOSITORY_NAME:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$IMAGE_TAG

# Step 5: Push image to ECR
echo -e "${YELLOW}Pushing image to ECR...${NC}"
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$IMAGE_TAG

# Step 6: Create Secrets in Secrets Manager (if they don't exist)
echo -e "${YELLOW}Setting up secrets in Secrets Manager...${NC}"

# AWS Access Key
if ! aws secretsmanager describe-secret --secret-id rfp-proposal-generator/aws-access-key --region $AWS_REGION > /dev/null 2>&1; then
    echo -e "${YELLOW}Please enter your AWS Access Key ID: ${NC}"
    read -s AWS_ACCESS_KEY
    aws secretsmanager create-secret \
        --name rfp-proposal-generator/aws-access-key \
        --secret-string "$AWS_ACCESS_KEY" \
        --region $AWS_REGION
fi

# AWS Secret Key
if ! aws secretsmanager describe-secret --secret-id rfp-proposal-generator/aws-secret-key --region $AWS_REGION > /dev/null 2>&1; then
    echo -e "${YELLOW}Please enter your AWS Secret Access Key: ${NC}"
    read -s AWS_SECRET_KEY
    aws secretsmanager create-secret \
        --name rfp-proposal-generator/aws-secret-key \
        --secret-string "$AWS_SECRET_KEY" \
        --region $AWS_REGION
fi

# Anthropic API Key
if ! aws secretsmanager describe-secret --secret-id rfp-proposal-generator/anthropic-api-key --region $AWS_REGION > /dev/null 2>&1; then
    echo -e "${YELLOW}Please enter your Anthropic API Key: ${NC}"
    read -s ANTHROPIC_KEY
    aws secretsmanager create-secret \
        --name rfp-proposal-generator/anthropic-api-key \
        --secret-string "$ANTHROPIC_KEY" \
        --region $AWS_REGION
fi

# Step 7: Deploy CloudFormation stack
echo -e "${YELLOW}Deploying CloudFormation stack...${NC}"
IMAGE_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$IMAGE_TAG"

# Get VPC and Subnet IDs (you may need to customize this)
VPC_ID=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query Vpcs[0].VpcId --output text --region $AWS_REGION)
SUBNET_IDS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID --query Subnets[0:2].SubnetId --output text --region $AWS_REGION | tr '\t' ',')

aws cloudformation deploy \
    --template-file aws/cloudformation-template.yaml \
    --stack-name $ENVIRONMENT-rfp-proposal-generator \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        VpcId=$VPC_ID \
        SubnetIds=$SUBNET_IDS \
        ContainerImage=$IMAGE_URI \
        Environment=$ENVIRONMENT \
        UseBedrock=true \
    --region $AWS_REGION

# Step 8: Get outputs
echo -e "${GREEN}Deployment complete!${NC}"
echo -e "${YELLOW}Stack Outputs:${NC}"
aws cloudformation describe-stacks \
    --stack-name $ENVIRONMENT-rfp-proposal-generator \
    --query 'Stacks[0].Outputs' \
    --output table \
    --region $AWS_REGION

echo -e "${GREEN}=== Deployment Successful ===${NC}"
echo -e "${YELLOW}Your API is now available at the Load Balancer URL shown above.${NC}"