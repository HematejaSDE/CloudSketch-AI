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


# EC2 Instance - Web application server
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 (update for your region)
  instance_type = "t2.micro"  # Free tier eligible

  tags = {
    Name = "web_server"
    Purpose = "Web application server"
  }
}


# RDS Database - MySQL database
resource "aws_db_instance" "database" {
  identifier           = "database"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"  # Free tier eligible
  allocated_storage    = 20
  storage_type         = "gp2"
  
  db_name  = "database"
  username = "admin"
  password = "change-me-in-production"  # Use AWS Secrets Manager in production
  
  skip_final_snapshot  = true

  tags = {
    Name = "database"
    Purpose = "MySQL database"
  }
}

