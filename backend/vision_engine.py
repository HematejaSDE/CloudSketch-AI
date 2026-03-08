"""Vision engine for analyzing architecture sketches using AWS Bedrock"""

import json
import base64
import boto3
from pathlib import Path
from typing import BinaryIO
from .models import ArchitectureSpec
from .config import (
    ALLOWED_AWS_SERVICES, 
    SERVICE_NAME_MAPPING,
    BEDROCK_MODEL_ID, 
    BEDROCK_REGION, 
    MAX_TOKENS, 
    TEMPERATURE
)


def load_vision_prompt() -> str:
    """Load the vision prompt from file"""
    prompt_path = Path(__file__).parent.parent / "prompts" / "vision_prompt.txt"
    return prompt_path.read_text()


def encode_image(image_file: BinaryIO) -> str:
    """Encode image to base64"""
    image_bytes = image_file.read()
    return base64.b64encode(image_bytes).decode('utf-8')


def extract_json_from_response(response_text: str) -> dict:
    """Extract JSON from Bedrock response, handling markdown code blocks"""
    # Try to parse directly first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract from markdown code block
    if "```json" in response_text:
        start = response_text.find("```json") + 7
        end = response_text.find("```", start)
        json_str = response_text[start:end].strip()
        return json.loads(json_str)
    elif "```" in response_text:
        start = response_text.find("```") + 3
        end = response_text.find("```", start)
        json_str = response_text[start:end].strip()
        return json.loads(json_str)
    
    # Last resort: try to find JSON object
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start != -1 and end > start:
        json_str = response_text[start:end]
        return json.loads(json_str)
    
    raise ValueError("Could not extract valid JSON from response")


def normalize_service_name(service_name: str) -> str:
    """
    Normalize service name to canonical form
    
    Args:
        service_name: Raw service name from AI
        
    Returns:
        Canonical service name or original if no mapping found
    """
    normalized = service_name.lower().strip()
    return SERVICE_NAME_MAPPING.get(normalized, service_name)


def filter_services(spec_dict: dict) -> dict:
    """Filter out services not in whitelist and normalize service names"""
    filtered_services = []
    for service in spec_dict.get('services', []):
        # Normalize service name
        original_name = service['aws_service']
        normalized_name = normalize_service_name(original_name)
        service['aws_service'] = normalized_name
        
        # Only keep if in whitelist
        if normalized_name in ALLOWED_AWS_SERVICES:
            filtered_services.append(service)
    
    spec_dict['services'] = filtered_services
    
    # Filter connections to only include valid service IDs
    valid_ids = {s['id'] for s in filtered_services}
    filtered_connections = []
    for conn in spec_dict.get('connections', []):
        if conn['from_service'] in valid_ids and conn['to_service'] in valid_ids:
            filtered_connections.append(conn)
    
    spec_dict['connections'] = filtered_connections
    return spec_dict


def analyze_image(image_file: BinaryIO) -> ArchitectureSpec:
    """
    Analyze architecture sketch using AWS Bedrock Vision
    
    Args:
        image_file: Binary file object of the uploaded image
        
    Returns:
        ArchitectureSpec: Validated architecture specification
    """
    # Reset file pointer
    image_file.seek(0)
    
    # Encode image
    image_base64 = encode_image(image_file)
    
    # Load prompt
    prompt = load_vision_prompt()
    
    # Initialize Bedrock client
    bedrock = boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)
    
    # Prepare request
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    # Call Bedrock
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps(request_body)
    )
    
    # Parse response
    response_body = json.loads(response['body'].read())
    response_text = response_body['content'][0]['text']
    
    # Extract JSON
    spec_dict = extract_json_from_response(response_text)
    
    # Filter services against whitelist
    spec_dict = filter_services(spec_dict)
    
    # Validate with Pydantic
    spec = ArchitectureSpec(**spec_dict)
    
    return spec
