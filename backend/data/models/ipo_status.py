from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class IPOStatus(Base):
    """Model for IPO statuses."""
    __tablename__ = 'ipo_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_ar = Column(String)

    # Relationships
    ipos = relationship("IPO", back_populates="ipo_status")
