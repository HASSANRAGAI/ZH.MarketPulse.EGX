#!/usr/bin/env python3
"""
Run the FastAPI server for ZH.MarketPulse.EGX Collector Microservice
"""

import uvicorn
from collector.api import app

if __name__ == "__main__":
    uvicorn.run(
        "collector.api.main:app",
        host="0.0.0.0",
        port=8001,  # Different port for microservice
        reload=True,
        log_level="info"
    )