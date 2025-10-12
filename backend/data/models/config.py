from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from shared.db_engine import Base

class Config(Base):
    """Model for storing configuration settings in database."""
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)  # e.g., 'retry.max_attempts'
    value = Column(Text, nullable=False)  # JSON string for complex values
    value_type = Column(String, nullable=False)  # 'str', 'int', 'float', 'bool', 'list', 'dict'
    category = Column(String, nullable=False, index=True)  # e.g., 'retry', 'scraping', 'ai'
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Config(key='{self.key}', value='{self.value}', category='{self.category}')>"