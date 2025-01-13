resource "aws_iam_policy" "github_actions_policy" {
  name        = "${var.project_name}-${var.env}-iam-policy-actions"
  description = "Policy for GitHub Actions to manage Terraform resources"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # S3 バケットアクセス権限
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::todo-list-app-${var.env}-s3-terraform-state",
          "arn:aws:s3:::todo-list-app-${var.env}-s3-terraform-state/*"
        ]
      },
      # DynamoDB テーブルアクセス権限
      {
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ],
        Resource = "arn:aws:dynamodb:ap-northeast-1:031869840243:table/terraform-lock-table"
      },
      # 必要な AWS リソースの操作権限（例: EC2, RDS, etc）
      {
        Effect = "Allow",
        Action = [
          "ec2:*",
          "rds:*",
          "iam:*"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "github_actions_role" {
  name               = "${var.project_name}-${var.env}-iam-role-actions"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = {
          Federated = "arn:aws:iam::031869840243:oidc-provider/token.actions.githubusercontent.com"
        },
        Action    = "sts:AssumeRole",
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
            "token.actions.githubusercontent.com:sub": "repo:shomakobayashi/todo-list-app:environment:${var.env}"
          }
        }
      }
    ]
  })
}

# ポリシーを IAM ロールにアタッチ
resource "aws_iam_role_policy_attachment" "github_actions_policy_attach" {
  role       = aws_iam_role.github_actions_role.name
  policy_arn = aws_iam_policy.github_actions_policy.arn
}

# GithubActionsユーザー
resource "aws_iam_user" "github_actions_user" {
  name = "${var.project_name}-${var.env}-iam-user-actions"
  path = "/"
}

# アクセスキーの作成
resource "aws_iam_access_key" "github_actions_access_key" {
  user = aws_iam_user.github_actions_user.name
}
