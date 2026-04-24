# VPC Module
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  environment        = var.environment
  project_name       = var.project_name
}

# Security Groups Module
module "security_groups" {
  source = "./modules/security_groups"

  vpc_id        = module.vpc.vpc_id
  vpc_cidr      = var.vpc_cidr
  environment   = var.environment
  project_name  = var.project_name
}

# Cognito Module (Authentication)
module "cognito" {
  source = "./modules/cognito"

  environment  = var.environment
  project_name = var.project_name
}

# ECR Module (Container Registry)
module "ecr" {
  source = "./modules/ecr"

  environment  = var.environment
  project_name = var.project_name
}

# Secrets Manager Module
module "secrets" {
  source = "./modules/secrets"

  environment  = var.environment
  project_name = var.project_name
}

# ECS Module (API Service)
module "ecs_api" {
  source = "./modules/ecs"

  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnet_ids
  security_group_id   = module.security_groups.api_sg_id
  ecr_repository_url = module.ecr.api_repository_url
  environment         = var.environment
  project_name        = var.project_name
  service_name        = "api"
  container_cpu       = var.container_cpu
  container_memory    = var.container_memory
  desired_count       = var.desired_count
  secrets_arn         = module.secrets.secrets_arn
  enable_bedrock      = var.enable_bedrock
}

# ECS Module (UI Service)
module "ecs_ui" {
  source = "./modules/ecs"

  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnet_ids
  security_group_id   = module.security_groups.ui_sg_id
  ecr_repository_url = module.ecr.ui_repository_url
  environment         = var.environment
  project_name        = var.project_name
  service_name        = "ui"
  container_cpu       = 512
  container_memory    = 1024
  desired_count       = 2
  secrets_arn         = module.cognito.user_pool_client_secrets_arn
  enable_bedrock      = false
  environment_vars = {
    NEXT_PUBLIC_COGNITO_USER_POOL_ID = module.cognito.user_pool_id
    NEXT_PUBLIC_COGNITO_CLIENT_ID     = module.cognito.user_pool_client_id
    NEXT_PUBLIC_COGNITO_REGION        = var.aws_region
    NEXT_PUBLIC_API_URL               = module.alb.api_dns_name
  }
}

# Application Load Balancer Module
module "alb" {
  source = "./modules/alb"

  vpc_id             = module.vpc.vpc_id
  public_subnet_ids  = module.vpc.public_subnet_ids
  security_group_ids = [module.security_groups.alb_sg_id]
  environment        = var.environment
  project_name       = var.project_name
  domain_name        = var.domain_name
  certificate_arn    = var.certificate_arn
}

# WAF Module (Web Application Firewall)
module "waf" {
  source = "./modules/waf"

  alb_arn      = module.alb.alb_arn
  environment  = var.environment
  project_name = var.project_name
}

# Route53 Module (DNS)
module "route53" {
  source = "./modules/route53"

  domain_name     = var.domain_name
  alb_dns_name    = module.alb.alb_dns_name
  alb_zone_id    = module.alb.alb_zone_id
  environment    = var.environment
  project_name   = var.project_name
  certificate_arn = var.certificate_arn
}

# CloudWatch Alarms and Dashboards
module "monitoring" {
  source = "./modules/monitoring"

  ecs_cluster_arn = module.ecs_api.cluster_arn
  ecs_service_arn = module.ecs_api.service_arn
  alb_arn         = module.alb.alb_arn
  environment     = var.environment
  project_name    = var.project_name
}

# Outputs
output "api_url" {
  description = "API endpoint URL"
  value       = module.alb.api_url
}

output "ui_url" {
  description = "UI endpoint URL"
  value       = module.alb.ui_url
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = module.cognito.user_pool_id
}

output "cognito_client_id" {
  description = "Cognito Client ID"
  value       = module.cognito.user_pool_client_id
}

output "ecr_api_repository_url" {
  description = "ECR API repository URL"
  value       = module.ecr.api_repository_url
}

output "ecr_ui_repository_url" {
  description = "ECR UI repository URL"
  value       = module.ecr.ui_repository_url
}