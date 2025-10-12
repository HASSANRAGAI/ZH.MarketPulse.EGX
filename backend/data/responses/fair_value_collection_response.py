"""
Pydantic models for fair value API responses.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .fair_value_response import FairValueResponse

class FairValueCollectionResponse(BaseModel):
    success: bool
    message: str
    fair_values_collected: Optional[list[FairValueResponse]] = None
    timestamp: datetime
    service: str = "collector"
