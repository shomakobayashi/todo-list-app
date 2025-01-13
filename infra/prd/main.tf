terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  required_version = ">= 1.2.0"

  backend "s3" {
    bucket = "todo-list-${var.env}-s3-terraform-state"        # 作成したS3バケット名
    key = "terraform.tfstate"                   # 状態ファイルのキー
    region = "ap-northeast-1"                     # S3バケットのリージョン
    dynamodb_table = "terraform-lock-table"               # 作成したDynamoDBテーブル名
    encrypt = true                                  # 状態ファイルの暗号化
  }
}

  provider "aws" {
    region = var.region
}
