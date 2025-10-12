from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class SourceType(Base):
    """Model for source types."""
    __tablename__ = 'source_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_ar = Column(String)

    # Relationships
    sources = relationship("Source", back_populates="type")
