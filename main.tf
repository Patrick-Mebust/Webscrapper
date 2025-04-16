# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Get the default VPC
data "aws_vpc" "default" {
  default = true
}

# Create an S3 bucket
resource "aws_s3_bucket" "example" {
  bucket = "terraform-tutorial-bucket-${random_id.bucket_suffix.hex}"
  
  tags = {
    Name        = "terraform-example-bucket"
    Environment = var.environment
  }
}

# Enable versioning for the S3 bucket
resource "aws_s3_bucket_versioning" "example" {
  bucket = aws_s3_bucket.example.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Add lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# Generate random suffix for bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 4
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

# Create SNS Topic
resource "aws_sns_topic" "bucket_updates" {
  name = "s3-bucket-updates"
}

# Add S3 bucket notification
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.example.id

  topic {
    topic_arn     = aws_sns_topic.bucket_updates.arn
    events        = ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
    filter_suffix = ".txt"
  }
}

# SNS Topic Policy
resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.bucket_updates.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowS3BucketNotifications"
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.bucket_updates.arn
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.current.account_id
          }
          ArnLike = {
            "aws:SourceArn" = aws_s3_bucket.example.arn
          }
        }
      }
    ]
  })
}

# Get current AWS account ID
data "aws_caller_identity" "current" {}
