from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class Recommendation(Base):
    """Model for recommendations."""
    __tablename__ = 'recommendations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_ar = Column(String)

    # Relationships
    fair_values = relationship("FairValue", back_populates="recommendation")
