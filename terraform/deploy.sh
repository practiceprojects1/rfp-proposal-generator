#!/bin/bash

# Terraform Deployment Script for RFP Proposal Generator
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== RFP Proposal Generator Terraform Deployment ===${NC}"

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Terraform is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check AWS authentication
echo -e "${YELLOW}Checking AWS authentication...${NC}"
aws sts get-caller-identity > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}AWS authentication failed. Please run 'aws configure' first.${NC}"
    exit 1
fi
echo -e "${GREEN}AWS authentication successful${NC}"

# Initialize Terraform
echo -e "${YELLOW}Initializing Terraform...${NC}"
terraform init

# Validate configuration
echo -e "${YELLOW}Validating Terraform configuration...${NC}"
terraform validate

# Format check
echo -e "${YELLOW}Checking Terraform format...${NC}"
terraform fmt -check

# Plan deployment
echo -e "${YELLOW}Creating execution plan...${NC}"
terraform plan -out=tfplan

# Ask for confirmation
echo -e "${YELLOW}Do you want to apply these changes? (yes/no)${NC}"
read -r response
if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Apply changes
echo -e "${YELLOW}Applying Terraform configuration...${NC}"
terraform apply tfplan

# Get outputs
echo -e "${GREEN}Deployment complete!${NC}"
echo -e "${YELLOW}Infrastructure Outputs:${NC}"
terraform output -json

echo -e "${GREEN}=== Deployment Successful ===${NC}"