from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class Source(Base):
    """Model for sources."""
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_ar = Column(String)
    type_id = Column(Integer, ForeignKey('source_types.id'))

    # Relationships
    type = relationship("SourceType", back_populates="sources")
    fair_values = relationship("FairValue", back_populates="source")
