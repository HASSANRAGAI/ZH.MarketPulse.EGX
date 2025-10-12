from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from shared.db_engine import Base

class News(Base):
    """Model for news articles from various sources."""
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), index=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    summary = Column(Text)
    source = Column(String, nullable=False)  # Mubasher, Arab Finance, Alborsaanews
    url = Column(String, unique=True)
    published_at = Column(DateTime, nullable=False, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    # Labeling fields
    sentiment = Column(String)  # positive, negative, neutral
    topic = Column(String)  # revenue-beat, expansion, new-factory, etc.
    confidence_score = Column(Float)  # AI confidence in labeling

    # Additional metadata
    tags = Column(JSON)  # Store tags as JSON array
    language = Column(String, default='ar')  # Arabic by default

    # Relationships
    stock = relationship("Stock", back_populates="news")