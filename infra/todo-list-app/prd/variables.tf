variable "env" {
  default   = "prd"
  type      = string
}

variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "region" {
  description = "AWSリージョン"
  default     = "ap-northeast-1"
}

variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  default     = "10.0.0.0/16"
}

variable "private_AZ_A" {
  type = string
}

# variable "domain_name" {
#   description = "Route53で管理するドメイン名"
# }
