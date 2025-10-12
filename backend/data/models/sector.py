from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class Sector(Base):
    """Model for sectors."""
    __tablename__ = 'sectors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_ar = Column(String)

    # Relationships
    stocks = relationship("Stock", back_populates="sector")
    ipos = relationship("IPO", back_populates="sector")
