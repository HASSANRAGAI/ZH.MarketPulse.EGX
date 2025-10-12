"""
Pydantic models for IPO API responses.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockBaseData(BaseModel):
    id: int
    symbol: str
    name: Optional[str]
    name_ar: Optional[str]
    market: Optional[str]
    sector: Optional[str]
    currency: Optional[str]

class IPOResponse(BaseModel):
    id: int
    name: Optional[str]
    name_ar: Optional[str]
    url: Optional[str]
    status: Optional[str]
    status_ar: Optional[str]
    attachment: Optional[str]
    type: Optional[str]
    type_ar: Optional[str]
    market: Optional[str]
    market_ar: Optional[str]
    sector: Optional[str]
    sector_ar: Optional[str]
    market_url: Optional[str]
    volume: Optional[int]
    announced_at: Optional[datetime]
    stock_symbol: Optional[str]
    stock_name: Optional[str]
    stock_name_ar: Optional[str]
    stock_base_data: Optional[StockBaseData]
