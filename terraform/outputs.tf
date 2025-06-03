output "smart_meter_dashboard_url" {
  description = "Smart Meter Dashboard URL"
  value       = "https://aws.saul-perdomo.workers.dev/"
}

output "aurora_cluster_endpoint" {
  description = "Aurora cluster endpoint"
  value       = aws_rds_cluster.aurora.endpoint
}

output "aurora_cluster_port" {
  description = "Aurora cluster port"
  value       = aws_rds_cluster.aurora.port
}

output "aurora_database_name" {
  description = "Aurora database name"
  value       = aws_rds_cluster.aurora.database_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = aws_subnet.public.id
}

output "private_subnet_id" {
  description = "Private subnet ID"
  value       = aws_subnet.private.id
}

output "aurora_security_group_id" {
  description = "Aurora security group ID"
  value       = aws_security_group.aurora.id
}

output "ecs_security_group_id" {
  description = "ECS security group ID"
  value       = aws_security_group.ecs.id
}

output "infrastructure_summary" {
  description = "Complete infrastructure overview"
  value = {
    project_name    = var.project_name
    environment     = var.environment
    aurora_endpoint = aws_rds_cluster.aurora.endpoint
    ecs_cluster     = aws_ecs_cluster.main.name
    vpc_id          = aws_vpc.main.id
    database_type   = "Aurora Serverless v2 PostgreSQL"
    auto_scaling    = "${var.aurora_min_capacity} to ${var.aurora_max_capacity} ACUs"
  }
}
