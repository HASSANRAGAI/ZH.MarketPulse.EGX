from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class Market(Base):
    """Model for markets."""
    __tablename__ = 'markets'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_ar = Column(String)

    # Relationships
    stocks = relationship("Stock", back_populates="market")
    ipos = relationship("IPO", back_populates="market")
