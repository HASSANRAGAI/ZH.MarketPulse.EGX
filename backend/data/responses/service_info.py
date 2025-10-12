"""
Pydantic models for API responses.
"""

from pydantic import BaseModel
from typing import Dict

class ServiceInfo(BaseModel):
    service: str = "collector"
    description: str = "Stock data collection microservice"
    endpoints: Dict[str, str]
    version: str = "1.0.0"