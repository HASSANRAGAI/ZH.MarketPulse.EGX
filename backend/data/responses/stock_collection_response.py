"""
Pydantic models for API responses.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .stock_response import StockResponse

class StockCollectionResponse(BaseModel):
    success: bool
    message: str
    stocks_collected: Optional[list[StockResponse]] = None
    timestamp: datetime
    service: str = "collector"
