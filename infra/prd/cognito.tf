resource "aws_cognito_user_pool" "main" {
  name = "${var.project_name}-user-pool"

  # パスワードポリシー
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = true
  }

  # ユーザー登録時の検証方法
  auto_verified_attributes = ["email"]

  # 管理者の確認が必要なフロー
  admin_create_user_config {
    allow_admin_create_user_only = true
  }

  tags = {
    Environment = var.environment
  }
}
