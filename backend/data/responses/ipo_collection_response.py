"""
Pydantic models for IPO API responses.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .ipo_response import IPOResponse

class IPOCollectionResponse(BaseModel):
    success: bool
    message: str
    ipos_collected: Optional[list[IPOResponse]] = None
    timestamp: datetime
    service: str = "collector"
