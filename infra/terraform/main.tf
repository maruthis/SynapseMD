variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

# Stub for AWS reference topology — extend per enterprise-architecture.md §12

output "platform_note" {
  value = "Deploy ECS Fargate services, HealthLake, Aurora, MSK, and Vault per docs/enterprise-architecture.md"
}
