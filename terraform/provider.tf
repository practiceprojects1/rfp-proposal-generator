provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "RFP Proposal Generator"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}