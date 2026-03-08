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


# S3 Bucket - Static website hosting
resource "aws_s3_bucket" "website_bucket" {
  bucket = "website_bucket-${random_id.bucket_suffix.hex}"

  tags = {
    Name = "website_bucket"
    Purpose = "Static website hosting"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

