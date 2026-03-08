"""Manual validation script for testing the pipeline"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.models import Service, ArchitectureSpec
from backend.terraform_generator import generate_terraform


def test_ec2_rds_pattern():
    """Test EC2 + RDS architecture pattern"""
    print("=" * 60)
    print("TEST 1: EC2 + RDS Pattern")
    print("=" * 60)
    
    spec = ArchitectureSpec(
        services=[
            Service(
                id="web_server",
                aws_service="EC2",
                purpose="Web application server",
                network_scope="public"
            ),
            Service(
                id="database",
                aws_service="RDS",
                purpose="MySQL database",
                network_scope="private"
            )
        ],
        connections=[
            {
                "from_service": "web_server",
                "to_service": "database",
                "interaction_type": "data_flow"
            }
        ]
    )
    
    print(f"✓ Services: {len(spec.services)}")
    print(f"✓ Connections: {len(spec.connections)}")
    print(f"✓ Service IDs unique: {len(set(s.id for s in spec.services)) == len(spec.services)}")
    
    terraform = generate_terraform(spec)
    print(f"✓ Terraform generated: {len(terraform)} characters")
    print(f"✓ Contains aws_instance: {'aws_instance' in terraform}")
    print(f"✓ Contains aws_db_instance: {'aws_db_instance' in terraform}")
    
    # Save to file for terraform validate
    output_file = Path(__file__).parent / "test_output_ec2_rds.tf"
    output_file.write_text(terraform)
    print(f"✓ Saved to: {output_file}")
    print()
    return terraform


def test_lambda_api_gateway_pattern():
    """Test Lambda + API Gateway pattern"""
    print("=" * 60)
    print("TEST 2: Lambda + API Gateway Pattern")
    print("=" * 60)
    
    spec = ArchitectureSpec(
        services=[
            Service(
                id="api",
                aws_service="API Gateway",
                purpose="REST API endpoint",
                network_scope="public"
            ),
            Service(
                id="function",
                aws_service="Lambda",
                purpose="Business logic handler",
                network_scope="private"
            )
        ],
        connections=[
            {
                "from_service": "api",
                "to_service": "function",
                "interaction_type": "event_trigger"
            }
        ]
    )
    
    print(f"✓ Services: {len(spec.services)}")
    print(f"✓ Connections: {len(spec.connections)}")
    
    terraform = generate_terraform(spec)
    print(f"✓ Terraform generated: {len(terraform)} characters")
    print(f"✓ Contains aws_lambda_function: {'aws_lambda_function' in terraform}")
    
    output_file = Path(__file__).parent / "test_output_lambda_api.tf"
    output_file.write_text(terraform)
    print(f"✓ Saved to: {output_file}")
    print()
    return terraform


def test_s3_static_site_pattern():
    """Test S3 static website pattern"""
    print("=" * 60)
    print("TEST 3: S3 Static Website Pattern")
    print("=" * 60)
    
    spec = ArchitectureSpec(
        services=[
            Service(
                id="website_bucket",
                aws_service="S3",
                purpose="Static website hosting",
                network_scope="public"
            )
        ],
        connections=[]
    )
    
    print(f"✓ Services: {len(spec.services)}")
    print(f"✓ Connections: {len(spec.connections)}")
    
    terraform = generate_terraform(spec)
    print(f"✓ Terraform generated: {len(terraform)} characters")
    print(f"✓ Contains aws_s3_bucket: {'aws_s3_bucket' in terraform}")
    
    output_file = Path(__file__).parent / "test_output_s3_static.tf"
    output_file.write_text(terraform)
    print(f"✓ Saved to: {output_file}")
    print()
    return terraform


def test_json_integrity():
    """Test JSON validation rules"""
    print("=" * 60)
    print("TEST 4: JSON Integrity Checks")
    print("=" * 60)
    
    # Test 1: Duplicate IDs should fail
    try:
        ArchitectureSpec(
            services=[
                Service(id="server", aws_service="EC2", purpose="Test", network_scope="public"),
                Service(id="server", aws_service="RDS", purpose="Test", network_scope="private")
            ],
            connections=[]
        )
        print("✗ FAILED: Duplicate IDs not caught")
    except ValueError:
        print("✓ Duplicate IDs rejected")
    
    # Test 2: Invalid connection references should fail
    try:
        ArchitectureSpec(
            services=[
                Service(id="server", aws_service="EC2", purpose="Test", network_scope="public")
            ],
            connections=[
                {"from_service": "server", "to_service": "nonexistent", "interaction_type": "api_call"}
            ]
        )
        print("✗ FAILED: Invalid connection not caught")
    except ValueError:
        print("✓ Invalid connections rejected")
    
    # Test 3: Invalid network scope should fail
    try:
        Service(id="test", aws_service="EC2", purpose="Test", network_scope="invalid")
        print("✗ FAILED: Invalid network scope not caught")
    except ValueError:
        print("✓ Invalid network scope rejected")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CLOUDSKETCH AI - STABILITY GATE 1 VALIDATION")
    print("=" * 60 + "\n")
    
    # Run all tests
    test_json_integrity()
    test_ec2_rds_pattern()
    test_lambda_api_gateway_pattern()
    test_s3_static_site_pattern()
    
    print("=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'terraform init' in tests/ directory")
    print("2. Run 'terraform validate' on generated .tf files")
    print("3. Test with Streamlit UI: streamlit run frontend/app.py")
    print()
