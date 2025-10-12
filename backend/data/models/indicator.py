from sqlalchemy import Column, Integer, Float, DateTime, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class Indicator(Base):
    """Model for technical indicators calculated from price data."""
    __tablename__ = 'indicators'

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Technical indicators
    rsi = Column(Float)  # Relative Strength Index
    sma_20 = Column(Float)  # Simple Moving Average 20
    sma_50 = Column(Float)  # Simple Moving Average 50
    ema_12 = Column(Float)  # Exponential Moving Average 12
    ema_26 = Column(Float)  # Exponential Moving Average 26
    macd = Column(Float)  # MACD line
    macd_signal = Column(Float)  # MACD signal line
    macd_histogram = Column(Float)  # MACD histogram
    bollinger_upper = Column(Float)  # Bollinger Band upper
    bollinger_lower = Column(Float)  # Bollinger Band lower
    volume_sma = Column(Float)  # Volume SMA

    # Turning point detection
    is_turning_point = Column(Boolean, default=False)
    direction = Column(String)  # 'up', 'down', or None
    strength = Column(Float)  # Strength of the turning point signal

    # Relationships
    stock = relationship("Stock", back_populates="indicators")