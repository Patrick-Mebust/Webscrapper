# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}

# Create a security group
resource "aws_security_group" "example" {
  name        = "terraform-example-sg"
  description = "Security group for Terraform example instance"

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
  ami           = "ami-0c55b159cbfafe1f0"  # Ubuntu 20.04 LTS AMI ID
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.example.id]

  tags = {
    Name        = "terraform-example"
    Environment = var.environment
  }
}
