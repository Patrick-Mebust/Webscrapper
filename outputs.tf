output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.example.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.example.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.example.public_dns
}

output "s3_bucket_name" {
  value = aws_s3_bucket.example.id
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.example.arn
}
