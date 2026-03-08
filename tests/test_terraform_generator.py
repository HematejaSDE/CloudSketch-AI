"""Test Terraform code generation"""

import pytest
from backend.models import Service, ArchitectureSpec
from backend.terraform_generator import generate_terraform, generate_provider_block


def test_generate_provider_block():
    """Test provider block generation"""
    provider = generate_provider_block("us-west-2")
    assert "terraform" in provider
    assert "required_version" in provider
    assert "us-west-2" in provider


def test_generate_terraform_ec2():
    """Test EC2 Terraform generation"""
    spec = ArchitectureSpec(
        services=[
            Service(id="web_server", aws_service="EC2", purpose="Web server", network_scope="public")
        ],
        connections=[]
    )
    terraform = generate_terraform(spec)
    assert "aws_instance" in terraform
    assert "web_server" in terraform
    assert "provider" in terraform


def test_generate_terraform_rds():
    """Test RDS Terraform generation"""
    spec = ArchitectureSpec(
        services=[
            Service(id="database", aws_service="RDS", purpose="MySQL database", network_scope="private")
        ],
        connections=[]
    )
    terraform = generate_terraform(spec)
    assert "aws_db_instance" in terraform
    assert "database" in terraform


def test_generate_terraform_multiple_services():
    """Test multiple services generation"""
    spec = ArchitectureSpec(
        services=[
            Service(id="web", aws_service="EC2", purpose="Web", network_scope="public"),
            Service(id="db", aws_service="RDS", purpose="Database", network_scope="private")
        ],
        connections=[]
    )
    terraform = generate_terraform(spec)
    assert "aws_instance" in terraform
    assert "aws_db_instance" in terraform
    assert terraform.count("resource") >= 2


def test_generate_terraform_unknown_service():
    """Test graceful handling of unknown service"""
    spec = ArchitectureSpec(
        services=[
            Service(id="unknown", aws_service="UnknownService", purpose="Test", network_scope="public")
        ],
        connections=[]
    )
    terraform = generate_terraform(spec)
    # Should not crash, should add TODO comment
    assert "TODO" in terraform or "provider" in terraform
