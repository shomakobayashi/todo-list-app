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
          "dynamodb:DescribeTable"
        ],
        Resource = "arn:aws:dynamodb:ap-northeast-1:031869840243:table/terraform-lock-table"
      },
      # EC2 関連リソースの操作権限
      {
        Effect = "Allow",
        Action = [
          "ec2:DescribeInstances",
          "ec2:RunInstances",
          "ec2:TerminateInstances",
          "ec2:DescribeSecurityGroups",
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:RevokeSecurityGroupIngress",
          "ec2:DescribeSubnets",
          "ec2:DescribeVpcs",
          "ec2:DescribeRouteTables",
          "ec2:CreateTags"
        ],
        Resource = "*"
      },
      # RDS 関連リソースの操作権限
      {
        Effect = "Allow",
        Action = [
          "rds:DescribeDBInstances",
          "rds:CreateDBInstance",
          "rds:ModifyDBInstance",
          "rds:DeleteDBInstance",
          "rds:DescribeDBSecurityGroups",
          "rds:CreateDBSecurityGroup",
          "rds:AuthorizeDBSecurityGroupIngress",
          "rds:RevokeDBSecurityGroupIngress"
        ],
        Resource = "*"
      },
      # ALB 関連リソースの操作権限
      {
        Effect = "Allow",
        Action = [
          "elasticloadbalancing:DescribeLoadBalancers",
          "elasticloadbalancing:CreateLoadBalancer",
          "elasticloadbalancing:DeleteLoadBalancer",
          "elasticloadbalancing:DescribeTargetGroups",
          "elasticloadbalancing:CreateTargetGroup",
          "elasticloadbalancing:DeleteTargetGroup",
          "elasticloadbalancing:ModifyTargetGroup",
          "elasticloadbalancing:RegisterTargets",
          "elasticloadbalancing:DeregisterTargets"
        ],
        Resource = "*"
      },
      # Route53 関連リソースの操作権限
      {
        Effect = "Allow",
        Action = [
          "route53:ChangeResourceRecordSets",
          "route53:GetChange",
          "route53:ListHostedZones",
          "route53:CreateHostedZone",
          "route53:DeleteHostedZone",
          "route53:ListResourceRecordSets"
        ],
        Resource = "*"
      },
      # ACM 関連リソースの操作権限
      {
        Effect = "Allow",
        Action = [
          "acm:RequestCertificate",
          "acm:DescribeCertificate",
          "acm:DeleteCertificate",
          "acm:ListCertificates",
          "acm:AddTagsToCertificate",
          "acm:RemoveTagsFromCertificate"
        ],
        Resource = "*"
      },
      # IAM 操作（ロールやポリシー管理）
      {
        Effect = "Allow",
        Action = [
          "iam:PassRole",
          "iam:GetRole",
          "iam:ListRoles",
          "iam:CreateRole",
          "iam:DeleteRole",
          "iam:AttachRolePolicy",
          "iam:DetachRolePolicy"
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

# GithubActionsユーザー
resource "aws_iam_user" "github_actions_user" {
  name = "${var.project_name}-${var.env}-iam-user-actions"
  path = "/"
}

# アクセスキーの作成
resource "aws_iam_access_key" "github_actions_access_key" {
  user = aws_iam_user.github_actions_user.name
}
