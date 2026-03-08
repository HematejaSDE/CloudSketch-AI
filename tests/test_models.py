"""Test data models and validation"""

import pytest
from backend.models import Service, Connection, ArchitectureSpec


def test_service_valid():
    """Test valid service creation"""
    service = Service(
        id="web_server",
        aws_service="EC2",
        purpose="Web application server",
        network_scope="public"
    )
    assert service.id == "web_server"
    assert service.aws_service == "EC2"


def test_service_invalid_network_scope():
    """Test invalid network scope rejection"""
    with pytest.raises(ValueError):
        Service(
            id="web_server",
            aws_service="EC2",
            purpose="Web server",
            network_scope="invalid"
        )


def test_architecture_spec_unique_ids():
    """Test duplicate service ID rejection"""
    with pytest.raises(ValueError):
        ArchitectureSpec(
            services=[
                Service(id="server1", aws_service="EC2", purpose="Web", network_scope="public"),
                Service(id="server1", aws_service="RDS", purpose="DB", network_scope="private")
            ],
            connections=[]
        )


def test_architecture_spec_connection_validation():
    """Test connection references valid services"""
    with pytest.raises(ValueError):
        ArchitectureSpec(
            services=[
                Service(id="server1", aws_service="EC2", purpose="Web", network_scope="public")
            ],
            connections=[
                Connection(from_service="server1", to_service="nonexistent", interaction_type="api_call")
            ]
        )


def test_architecture_spec_valid():
    """Test valid architecture spec"""
    spec = ArchitectureSpec(
        services=[
            Service(id="web", aws_service="EC2", purpose="Web server", network_scope="public"),
            Service(id="db", aws_service="RDS", purpose="Database", network_scope="private")
        ],
        connections=[
            Connection(from_service="web", to_service="db", interaction_type="data_flow")
        ]
    )
    assert len(spec.services) == 2
    assert len(spec.connections) == 1
