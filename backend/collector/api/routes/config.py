"""
Configuration endpoints.
"""

from fastapi import HTTPException
from datetime import datetime

from shared import config_manager
from shared.custom_logging import logger, log_error_with_exception

async def get_collector_config():
    """Get collector-specific configuration."""
    try:
        config = config_manager.get_config()
        collector_config = {
            "mubasher_endpoints": config.get("mubasher_endpoints", {}),
            "retry": config.get("retry", {}),
            "scraping": config.get("scraping", {})
        }
        return {
            "service": "collector",
            "config": collector_config,
            "timestamp": datetime.now()
        }
    except Exception as e:
        log_error_with_exception("Failed to get collector config")
        raise HTTPException(status_code=500, detail="Failed to retrieve configuration")