# IAMポリシー
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
          "arn:aws:s3:::todo-list-${var.env}-s3-terraform-state",
          "arn:aws:s3:::todo-list-${var.env}-s3-terraform-state/*"
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
          "dynamodb:Query",
          "dynamodb:DescribeContinuousBackups",
          "dynamodb:DescribeTable",
          "dynamodb:ListTagsOfResource"
        ],
        Resource = "arn:aws:dynamodb:ap-northeast-1:031869840243:table/terraform-lock-table"
      },
      # Cognito 権限
      {
        Effect = "Allow",
        Action = [
          "cognito-idp:*"
        ],
        Resource = "*"
      },
      # IAM 権限
      {
        Effect = "Allow",
        Action = [
          "iam:GetPolicy",
          "iam:GetPolicyVersion",
          "iam:ListAttachedRolePolicies",
          "iam:GetUser",
          "iam:ListRolePolicies",
          "iam:GetRole",
          "iam:CreateRole",
          "iam:DeleteRole",
          "iam:PutRolePolicy",
          "iam:DeleteRolePolicy",
          "iam:AttachRolePolicy",
          "iam:DetachRolePolicy",
          "iam:ListAccessKeys",
        ],
        Resource = "*"
      },
      # EC2 関連権限
      {
        Effect = "Allow",
        Action = [
          "ec2:*"
        ],
        Resource = "*"
      },
      # RDS 権限
      {
        Effect = "Allow",
        Action = [
          "rds:*"
        ],
        Resource = "*"
      },
      # ACM 権限
      {
        Effect = "Allow",
        Action = [
          "acm:*"
        ],
        Resource = "*"
      },
      # Route53 権限
      {
        Effect = "Allow",
        Action = [
          "route53:*"
        ],
        Resource = "*"
      },
      # ALB 関連権限
      {
        Effect = "Allow",
        Action = [
          "elasticloadbalancing:*",
          "elasticloadbalancingv2:*"
        ],
        Resource = "*"
      },
      # セキュリティグループ作成のための追加権限
      {
        Effect = "Allow",
        Action = [
          "ec2:CreateSecurityGroup",
          "ec2:DescribeSecurityGroups",
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:RevokeSecurityGroupIngress"
        ],
        Resource = "*"
      },
      # サブネット、ルートテーブル関連の権限
      {
        Effect = "Allow",
        Action = [
          "ec2:CreateSubnet",
          "ec2:DescribeSubnets",
          "ec2:CreateRoute",
          "ec2:CreateRouteTable",
          "ec2:AssociateRouteTable",
          "ec2:DescribeRouteTables"
        ],
        Resource = "*"
      }
    ]
  })
}

# IAMロール
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
        Action    = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          "StringLike": {
            "token.actions.githubusercontent.com:sub": "repo:shomakobayashi/todo-list-app:*"
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
