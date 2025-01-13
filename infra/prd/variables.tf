variable "env" {
  type = string
}

variable "private_AZ_A" {
  type = string
}

variable "region" {
  description = "AWSリージョン"
  default     = "ap-northeast-1"
}

variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  default     = "10.0.0.0/16"
}

variable "domain_name" {
  description = "Route53で管理するドメイン名"
}

variable "environment" {
  description = "環境名 (例: prd)"
  default     = "prd"
}

# RDS関連
variable "rds_db_name" {
  description = "RDSのデータベース名"
  default     = "todo_db"
}

variable "rds_username" {
  description = "RDSのユーザー名"
  default     = "admin"
}

variable "rds_password" {
  description = "RDSのパスワード"
  sensitive   = true
}

# ECSタスク関連
variable "ecs_task_cpu" {
  description = "ECSタスクのCPU"
  default     = "256"
}

variable "ecs_task_memory" {
  description = "ECSタスクのメモリ"
  default     = "512"
}