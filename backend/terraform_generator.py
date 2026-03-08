"""Terraform code generator using Jinja2 templates"""

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from .models import ArchitectureSpec


def get_template_environment():
    """Initialize Jinja2 environment with templates directory"""
    templates_dir = Path(__file__).parent.parent / "templates"
    return Environment(loader=FileSystemLoader(str(templates_dir)))


def generate_provider_block(region: str = "us-east-1") -> str:
    """Generate Terraform provider configuration"""
    return f"""terraform {{
  required_version = ">= 1.5"
  
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "{region}"
}}

"""


def generate_terraform(spec: ArchitectureSpec, region: str = "us-east-1") -> str:
    """
    Generate Terraform code from architecture specification
    
    Args:
        spec: Validated architecture specification
        region: AWS region for deployment
        
    Returns:
        Complete Terraform HCL code as string
    """
    env = get_template_environment()
    output = []
    
    # Add provider block
    output.append(generate_provider_block(region))
    
    # Generate resources for each service
    for service in spec.services:
        # Map AWS service name to template file
        template_name = f"{service.aws_service.lower().replace(' ', '_')}.j2"
        
        try:
            template = env.get_template(template_name)
            resource_code = template.render(service=service)
            output.append(resource_code)
            output.append("\n")
        except Exception as e:
            # If template not found, add comment
            output.append(f"# TODO: Template not found for {service.aws_service}\n")
            output.append(f"# Service: {service.id} - {service.purpose}\n\n")
    
    return "\n".join(output)
