"""Test vision engine JSON extraction and filtering"""

import pytest
from backend.vision_engine import extract_json_from_response, filter_services


def test_extract_json_direct():
    """Test direct JSON extraction"""
    response = '{"services": [], "connections": []}'
    result = extract_json_from_response(response)
    assert result == {"services": [], "connections": []}


def test_extract_json_from_markdown():
    """Test JSON extraction from markdown code block"""
    response = '''Here is the architecture:
```json
{"services": [{"id": "test", "aws_service": "EC2", "purpose": "test", "network_scope": "public"}], "connections": []}
```
'''
    result = extract_json_from_response(response)
    assert "services" in result
    assert len(result["services"]) == 1


def test_extract_json_from_text():
    """Test JSON extraction from mixed text"""
    response = 'Some text before {"services": [], "connections": []} some text after'
    result = extract_json_from_response(response)
    assert result == {"services": [], "connections": []}


def test_filter_services_whitelist():
    """Test service filtering against whitelist"""
    spec_dict = {
        "services": [
            {"id": "valid", "aws_service": "EC2", "purpose": "test", "network_scope": "public"},
            {"id": "invalid", "aws_service": "UnknownService", "purpose": "test", "network_scope": "public"}
        ],
        "connections": []
    }
    result = filter_services(spec_dict)
    assert len(result["services"]) == 1
    assert result["services"][0]["aws_service"] == "EC2"


def test_filter_connections_invalid_references():
    """Test connection filtering when service removed"""
    spec_dict = {
        "services": [
            {"id": "valid", "aws_service": "EC2", "purpose": "test", "network_scope": "public"}
        ],
        "connections": [
            {"from_service": "valid", "to_service": "removed", "interaction_type": "api_call"}
        ]
    }
    result = filter_services(spec_dict)
    assert len(result["connections"]) == 0
