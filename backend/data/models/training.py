from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from shared.db_engine import Base

class TrainingData(Base):
    """Model for prepared data used in AI training."""
    __tablename__ = 'training_data'

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Feature vector (technical indicators + news sentiment)
    features = Column(JSON, nullable=False)  # Store as JSON for flexibility

    # Target variables
    price_direction = Column(String)  # 'up', 'down', 'sideways'
    price_change_pct = Column(Float)  # Actual percentage change
    confidence = Column(Float)  # Prediction confidence

    # Source data references
    indicator_id = Column(Integer, ForeignKey('indicators.id'))
    news_ids = Column(JSON)  # Array of relevant news IDs

    # Training metadata
    is_training_sample = Column(Boolean, default=True)
    fold_id = Column(Integer)  # For cross-validation

    # Relationships
    stock = relationship("Stock")
