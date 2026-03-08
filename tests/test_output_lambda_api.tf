terraform {
  required_version = ">= 1.5"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}


# TODO: Template not found for API Gateway

# Service: api - REST API endpoint


# Lambda Function - Business logic handler
resource "aws_lambda_function" "function" {
  function_name = "function"
  role          = aws_iam_role.function_role.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  
  filename      = "lambda_function.zip"  # You need to provide this

  tags = {
    Name = "function"
    Purpose = "Business logic handler"
  }
}

resource "aws_iam_role" "function_role" {
  name = "function_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

