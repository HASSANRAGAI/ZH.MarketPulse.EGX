"""
Pydantic models for API responses.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockResponse(BaseModel):
    symbol: str
    name_en: str
    name_ar: str
    sector_en: str
    sector_ar: str
    market_en: str
    market_ar: str
    currency: Optional[str]
    profile_url: Optional[str]
    current_price: Optional[float]
    change_percentage: Optional[float]
    last_update: Optional[datetime]
    is_active: bool
