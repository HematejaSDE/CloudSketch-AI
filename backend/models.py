from pydantic import BaseModel, field_validator
from typing import List


class Service(BaseModel):
    id: str
    aws_service: str
    purpose: str
    network_scope: str  # public/private

    @field_validator('network_scope')
    @classmethod
    def validate_network_scope(cls, v):
        if v not in ['public', 'private']:
            raise ValueError('network_scope must be public or private')
        return v


class Connection(BaseModel):
    from_service: str
    to_service: str
    interaction_type: str


class ArchitectureSpec(BaseModel):
    services: List[Service]
    connections: List[Connection]

    @field_validator('services')
    @classmethod
    def validate_unique_ids(cls, v):
        ids = [s.id for s in v]
        if len(ids) != len(set(ids)):
            raise ValueError('Service IDs must be unique')
        return v

    @field_validator('connections')
    @classmethod
    def validate_connections(cls, v, info):
        if 'services' in info.data:
            service_ids = {s.id for s in info.data['services']}
            for conn in v:
                if conn.from_service not in service_ids:
                    raise ValueError(f'Connection from_service {conn.from_service} not found')
                if conn.to_service not in service_ids:
                    raise ValueError(f'Connection to_service {conn.to_service} not found')
        return v
