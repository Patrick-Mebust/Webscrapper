# Terraform Learning Project

This repository contains examples and best practices for learning Terraform. It demonstrates infrastructure as code (IaC) concepts using AWS as the cloud provider.

## Prerequisites

- Terraform (v1.11.3 or later)
- AWS CLI configured with appropriate credentials
- Basic understanding of AWS services

## Getting Started

1. Clone this repository
2. Run `terraform init`
3. Run `terraform plan`
4. Run `terraform apply`

## Security Note

This is a learning project. In a production environment, you should:
- Never commit AWS credentials to version control
- Use proper state management
- Implement proper security groups and network isolation
- Use workspaces for environment separation
