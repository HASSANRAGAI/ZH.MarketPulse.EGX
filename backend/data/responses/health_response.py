"""
Pydantic models for API responses.
"""

from pydantic import BaseModel
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    database: bool
    service: str = "collector"
    timestamp: datetime