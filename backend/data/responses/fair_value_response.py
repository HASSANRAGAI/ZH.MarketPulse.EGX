"""
Pydantic models for fair value API responses.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FairValueResponse(BaseModel):
    id: int
    symbol: str
    released_at: Optional[datetime]
    source: Optional[str]
    source_ar: Optional[str]
    recommendation: Optional[str]
    recommendation_ar: Optional[str]
    market: Optional[str]
    sector: Optional[str]
    market_url: Optional[str]
    value: Optional[float]
    price: Optional[float]
    last_price: Optional[float]
    change: Optional[float]
    change_percentage: Optional[float]
