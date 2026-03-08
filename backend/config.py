"""Configuration and constants for CloudSketch AI"""

ALLOWED_AWS_SERVICES = {
    "EC2",
    "RDS",
    "S3",
    "Lambda",
    "API Gateway",
    "ALB",
    "VPC",
    "ASG"
}

# Service name normalization mapping
# Maps various AI outputs to canonical service names
SERVICE_NAME_MAPPING = {
    # EC2 variations
    "ec2": "EC2",
    "amazon ec2": "EC2",
    "aws ec2": "EC2",
    "ec2 instance": "EC2",
    "compute": "EC2",
    "virtual machine": "EC2",
    "vm": "EC2",
    
    # RDS variations
    "rds": "RDS",
    "amazon rds": "RDS",
    "aws rds": "RDS",
    "database": "RDS",
    "mysql": "RDS",
    "postgres": "RDS",
    "postgresql": "RDS",
    
    # S3 variations
    "s3": "S3",
    "amazon s3": "S3",
    "aws s3": "S3",
    "storage": "S3",
    "bucket": "S3",
    
    # Lambda variations
    "lambda": "Lambda",
    "aws lambda": "Lambda",
    "amazon lambda": "Lambda",
    "function": "Lambda",
    "serverless": "Lambda",
    
    # API Gateway variations
    "api gateway": "API Gateway",
    "apigateway": "API Gateway",
    "api": "API Gateway",
    "rest api": "API Gateway",
    
    # ALB variations
    "alb": "ALB",
    "load balancer": "ALB",
    "application load balancer": "ALB",
    "elb": "ALB",
    
    # VPC variations
    "vpc": "VPC",
    "virtual private cloud": "VPC",
    "network": "VPC",
    
    # ASG variations
    "asg": "ASG",
    "auto scaling": "ASG",
    "autoscaling": "ASG",
    "auto scaling group": "ASG"
}

# Bedrock configuration
BEDROCK_MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"
BEDROCK_REGION = "us-east-1"
MAX_TOKENS = 4096
TEMPERATURE = 0.0
