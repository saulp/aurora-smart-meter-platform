variable "project_name" {
  description = "Smart Meter Management Platform"
  type        = string
  default     = "smart-meter"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "aurora_master_password" {
  description = "Master password for Aurora cluster"
  type        = string
  default     = "REDACTED"
  sensitive   = true
}

variable "aurora_min_capacity" {
  description = "Minimum Aurora Serverless v2 capacity"
  type        = number
  default     = 0.5
}

variable "aurora_max_capacity" {
  description = "Maximum Aurora Serverless v2 capacity"
  type        = number
  default     = 16
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "Smart Meter Management"
    Environment = "Production"
    Owner       = "Saul Perdomo"
    Purpose     = "Utility Industry Demo"
    Technology  = "Aurora Serverless v2"
  }
}
