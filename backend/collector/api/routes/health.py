"""
Health check endpoints.
"""

from fastapi import HTTPException
from datetime import datetime

from data import Config, HealthResponse
from shared import check_connection, get_session, log_error_with_exception

async def health_check():
    """Health check endpoint."""
    try:
        db_status = check_connection()

        # Also check if database is initialized
        db_initialized = False
        if db_status:
            try:
                with get_session() as session:
                    # Check if config table exists and has data
                    config_count = session.query(Config).count()
                    db_initialized = config_count > 0
            except Exception:
                db_initialized = False

        status = "healthy" if (db_status and db_initialized) else "unhealthy"

        return HealthResponse(
            status=status,
            database=db_status,
            timestamp=datetime.now()
        )
    except Exception as e:
        log_error_with_exception("Health check failed")
        raise HTTPException(status_code=500, detail="Health check failed")