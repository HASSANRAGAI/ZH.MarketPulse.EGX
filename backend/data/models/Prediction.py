from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from shared.db_engine import Base


class Prediction(Base):
    """Model for AI predictions."""
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    prediction_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Prediction results
    predicted_direction = Column(String, nullable=False)  # 'up', 'down', 'sideways'
    confidence_score = Column(Float, nullable=False)
    predicted_change_pct = Column(Float)

    # Model metadata
    model_version = Column(String)
    features_used = Column(JSON)

    # Actual outcome (filled later)
    actual_direction = Column(String)
    actual_change_pct = Column(Float)
    accuracy = Column(Float)  # 1.0 if correct, 0.0 if wrong

    # Relationships
    stock = relationship("Stock")