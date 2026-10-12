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
    return prompt_path.read_text(encoding="utf-8")


def detect_media_type(image_file: BinaryIO) -> str:
    """Detect image media type from attribute or header bytes"""
    # 1. Check if Streamlit UploadedFile has type attribute
    content_type = getattr(image_file, "type", None)
    if content_type in ["image/png", "image/jpeg", "image/webp", "image/gif"]:
        return content_type
    
    # 2. Check filename extension if available
    name = getattr(image_file, "name", "").lower()
    if name.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    elif name.endswith(".png"):
        return "image/png"
    elif name.endswith(".webp"):
        return "image/webp"
    elif name.endswith(".gif"):
        return "image/gif"
    
    # 3. Check header bytes
    image_file.seek(0)
    header = image_file.read(12)
    image_file.seek(0)
    if header.startswith(b'\x89PNG\r\n\x1a\n'):
        return "image/png"
    elif header.startswith(b'\xff\xd8\xff'):
        return "image/jpeg"
    elif header.startswith(b'RIFF') and header[8:12] == b'WEBP':
        return "image/webp"
    elif header.startswith((b'GIF87a', b'GIF89a')):
        return "image/gif"
    
    return "image/png"


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
    # Detect media type
    media_type = detect_media_type(image_file)
    
    # Reset file pointer
    image_file.seek(0)
    
    # Encode image
    image_base64 = encode_image(image_file)
    
    # Load prompt
    prompt = load_vision_prompt()
    
    # Initialize Bedrock client with configured region
    import os
    region = os.environ.get("AWS_DEFAULT_REGION") or BEDROCK_REGION
    bedrock = boto3.client('bedrock-runtime', region_name=region)
    
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
                            "media_type": media_type,
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
