# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Get the default VPC
data "aws_vpc" "default" {
  default = true
}

# Create a security group
resource "aws_security_group" "example" {
  name        = "terraform-example-sg"
  description = "Security group for Terraform example instance"
  vpc_id      = data.aws_vpc.default.id
  revoke_rules_on_delete = false

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "terraform-example-sg"
    Environment = var.environment
  }
}

# Resource - Define infrastructure components
resource "aws_instance" "example" {
  ami           = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS AMI ID for us-east-1
  instance_type = var.instance_type
  key_name      = "terraform-key"
  vpc_security_group_ids = [aws_security_group.example.id]

  tags = {
    Name        = "terraform-example"
    Environment = var.environment
  }

  # Wait for instance to be ready
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y openssh-server
              systemctl enable ssh
              systemctl start ssh
              EOF
}
