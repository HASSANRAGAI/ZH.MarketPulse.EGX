from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class Stock(Base):
    """Model for EGX stock information."""
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False, index=True)  # EGX symbol like HRHO
    name_en = Column(String, nullable=False)  # English name
    name_ar = Column(String)  # Arabic name
    reuters_code = Column(String, unique=True)  # Reuters code for the stock
    sector_id = Column(Integer, ForeignKey('sectors.id'), index=True)
    market_id = Column(Integer, ForeignKey('markets.id'), index=True)
    currency = Column(String, default="EGP")  # Trading currency
    profile_url = Column(String)  # Mubasher profile URL
    current_price = Column(Float)  # Latest price
    change_percentage = Column(Float)  # Latest change percentage
    last_update = Column(DateTime)  # Last update timestamp
    is_active = Column(Boolean, default=True)

    # Relationships
    prices = relationship("StockPrice", back_populates="stock", cascade="all, delete-orphan")
    news = relationship("News", back_populates="stock", cascade="all, delete-orphan")
    indicators = relationship("Indicator", back_populates="stock", cascade="all, delete-orphan")
    fair_values = relationship("FairValue", back_populates="stock", cascade="all, delete-orphan")
    sector = relationship("Sector", back_populates="stocks")
    market = relationship("Market", back_populates="stocks")
    ipos = relationship("IPO", back_populates="stock", cascade="all, delete-orphan")
