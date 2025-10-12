from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class IPOType(Base):
    """Model for IPO types."""
    __tablename__ = 'ipo_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_ar = Column(String)

    # Relationships
    ipos = relationship("IPO", back_populates="ipo_type")
