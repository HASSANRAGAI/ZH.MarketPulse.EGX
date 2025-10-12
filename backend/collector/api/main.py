#!/usr/bin/env python3
"""
FastAPI Application for ZH.MarketPulse.EGX
Provides REST API endpoints for data collection and management.
"""

import uvicorn
from .app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)