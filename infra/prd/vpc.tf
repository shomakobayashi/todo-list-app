# VPC
resource "aws_vpc" "aws_prd_vpc" {
  enable_dns_support   = true
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
}

# PublicSubnet
#----------------------------------------
resource "aws_subnet" "aws_prd_public_subnet" {
  vpc_id                  = aws_vpc.aws_prd_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-northeast-1a"
  map_public_ip_on_launch = true
}

#PrivateSubnet
resource "aws_subnet" "aws_prd_private_subnet" {
  vpc_id                  = aws_vpc.aws_prd_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "ap-northeast-1a"
  map_public_ip_on_launch = false
}

# IGW
resource "aws_internet_gateway" "aws_prd_igw" {
  vpc_id = aws_vpc.aws_prd_vpc.id
}

#RouteTable
resource "aws_route_table" "aws_prd_rtb" {
  vpc_id = aws_vpc.aws_prd_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.aws_prd_igw.id
  }
}

# サブネットにルートテーブルを紐づけ
resource "aws_route_table_association" "aws_prd_rt_assoc" {
  subnet_id      = aws_subnet.aws_prd_public_subnet.id
  route_table_id = aws_route_table.aws_prd_rtb.id
}
