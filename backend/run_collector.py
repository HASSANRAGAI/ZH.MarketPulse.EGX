#!/usr/bin/env python3
"""
Run the Collector Microservice
"""

import uvicorn
from collector.api.main import app

if __name__ == "__main__":
    uvicorn.run(
        "collector.api.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )