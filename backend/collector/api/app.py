"""
FastAPI application setup and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import shared as sh
from shared import logger
from data import entities, responses

from .routes import health_check, get_collector_config, collect_stocks, collect_stocks_sync, get_stocks, collect_fair_values, collect_fair_values_sync, get_fair_values, collect_ipos, collect_ipos_sync, get_ipos
from typing import List

# Create FastAPI app
app = FastAPI(
    title="ZH.MarketPulse.EGX - Collector Service",
    description="Microservice for collecting stock data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/health", response_model=responses.HealthResponse)(health_check)
app.get("/config")(get_collector_config)
app.post("/collect/stocks", response_model=responses.StockCollectionResponse)(collect_stocks)
app.get("/collect/stocksSync", response_model=responses.StockCollectionResponse)(collect_stocks_sync)
app.get("/stocks", response_model=List[responses.StockResponse])(get_stocks)
app.post("/collect/fairValues", response_model=responses.FairValueCollectionResponse)(collect_fair_values)
app.get("/collect/fairValuesSync", response_model=responses.FairValueCollectionResponse)(collect_fair_values_sync)
app.get("/fairValues", response_model=List[responses.FairValueResponse])(get_fair_values)
app.post("/collect/ipos", response_model=responses.IPOCollectionResponse)(collect_ipos)
app.get("/collect/iposSync", response_model=responses.IPOCollectionResponse)(collect_ipos_sync)
app.get("/ipos", response_model=List[responses.IPOResponse])(get_ipos)


@app.get("/", response_model=responses.ServiceInfo)
async def root():
    """Root endpoint with service information."""
    return responses.ServiceInfo(
        endpoints={
            "health": "/health",
            "collect_stocks": "POST /collect/stocks",
            "collect_stocks_sync": "GET /collect/stocksSync",
            "get_stocks": "GET /stocks",
            "collect_fair_values": "POST /collect/fairValues",
            "collect_fair_values_sync": "GET /collect/fairValuesSync",
            "get_fair_values": "GET /fairValues",
            "collect_ipos": "POST /collect/ipos",
            "collect_ipos_sync": "GET /collect/iposSync",
            "get_ipos": "GET /ipos",
            "config": "/config"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    logger.info("🚀 Starting Collector Microservice")

    # Initialize database if needed
    try:
        initializer = sh.DatabaseInitializer()
        if not initializer.initialize_database(force=True):
            logger.error("❌ Database initialization failed during startup")
            # Don't exit, let the service start but log the error
        else:
            logger.info("✅ Database initialized successfully")
    except Exception as e:
        sh.log_error_with_exception("❌ Database initialization failed during startup")

    # Check database connection
    if not sh.check_connection():
        logger.warning("⚠️ Database connection not available on startup")
    else:
        logger.info("✅ Database connection established")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    logger.info("🛑 Shutting down Collector Microservice")
