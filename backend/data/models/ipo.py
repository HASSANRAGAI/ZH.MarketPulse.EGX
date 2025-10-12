from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class IPO(Base):
    """Model for IPOs from Mubasher."""
    __tablename__ = 'ipos'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    name_ar = Column(String)
    url = Column(String)
    attachment = Column(String)
    sector_id = Column(Integer, ForeignKey('sectors.id'), index=True)
    market_id = Column(Integer, ForeignKey('markets.id'), index=True)
    type_id = Column(Integer, ForeignKey('ipo_types.id'), index=True)
    status_id = Column(Integer, ForeignKey('ipo_statuses.id'), index=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), index=True)
    volume = Column(Integer)
    announced_at = Column(DateTime)

    # Relationships
    sector = relationship("Sector", back_populates="ipos")
    market = relationship("Market", back_populates="ipos")
    ipo_type = relationship("IPOType", back_populates="ipos")
    ipo_status = relationship("IPOStatus", back_populates="ipos")
    stock = relationship("Stock", back_populates="ipos")
