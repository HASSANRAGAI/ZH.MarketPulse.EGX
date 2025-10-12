from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class FairValue(Base):
    """Model for fair value recommendations from Mubasher."""
    __tablename__ = 'fair_values'

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), index=True)
    released_at = Column(DateTime)
    source_id = Column(Integer, ForeignKey('sources.id'), index=True)
    recommendation_id = Column(Integer, ForeignKey('recommendations.id'), index=True)
    value = Column(Float)
    price = Column(Float)
    last_price = Column(Float)
    change = Column(Float)
    change_percentage = Column(Float)

    # Unique constraint on released_at, source_id, and stock_id
    __table_args__ = (UniqueConstraint('released_at', 'source_id', 'stock_id'),)

    # Relationships
    stock = relationship("Stock", back_populates="fair_values")
    source = relationship("Source", back_populates="fair_values")
    recommendation = relationship("Recommendation", back_populates="fair_values")
