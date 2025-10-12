from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import os
from contextlib import contextmanager

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
Base = declarative_base()  

def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close()

def import_all_models():
    """Import all models to register them with SQLAlchemy Base metadata."""
    # Import all model classes to register them with Base.metadata
    from data.models import Stock, StockPrice, News, Indicator, TrainingData, Prediction, Config, FairValue

def create_tables():
    """Create all tables defined in the Base metadata."""
    import_all_models()  # Import models first so they're registered
    Base.metadata.create_all(bind=engine)

def check_connection():
    """Check if the database connection is healthy."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False

@contextmanager
def get_session():
    """Context manager for manual database sessions."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
