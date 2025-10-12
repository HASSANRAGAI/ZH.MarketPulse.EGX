"""
Stock-related endpoints.
"""

from fastapi import HTTPException, BackgroundTasks
from typing import List
from datetime import datetime

from sqlalchemy import false

from shared import logger, log_error_with_exception, get_session
from ...StockCollector import stock_collector, run_stock_collection, run_get_stocks
from data import responses, Stock


async def collect_stocks(background_tasks: BackgroundTasks):
    """
    Trigger stock data collection from Mubasher API.

    This endpoint starts the stock collection process in the background
    and returns immediately with a status response.
    """
    try:
        logger.info("🚀 Starting stock collection via API")

        # Run collection in background
        background_tasks.add_task(run_stock_collection)

        return responses.StockCollectionResponse(
            success=True,
            message="Stock collection started in background",
            timestamp=datetime.now()
        )

    except Exception as e:
        log_error_with_exception("Failed to start stock collection")
        raise HTTPException(status_code=500, detail=f"Failed to start collection: {str(e)}")


async def collect_stocks_sync():
    """
    Trigger synchronous stock data collection from Mubasher API.

    This endpoint waits for the collection to complete before returning.
    Use with caution as it may take several minutes.
    """
    try:
        logger.info("🚀 Starting synchronous stock collection via API")

        # Run collection synchronously
        stocks_collected = await run_stock_collection()

        if stocks_collected == -1 or stocks_collected == 0:
            return responses.StockCollectionResponse(
            success=False,
            message="Stock collection failed or no stocks collected",
            timestamp=datetime.now()
        )

        stocks_response = await run_get_stocks()
        return responses.StockCollectionResponse(
            success=True,
            message="Stock collection completed successfully",
            stocks_collected=stocks_response,
            timestamp=datetime.now()
        )

    except Exception as e:
        log_error_with_exception("Stock collection failed")
        raise HTTPException(status_code=500, detail=f"Collection failed: {str(e)}")

async def get_stocks():
    """
    Get all collected stocks from the database.

    Returns:
        List of stock data
    """
    try:
        stocks_response = await run_get_stocks()
        logger.info(f"✅ Stock got from the Database: {len(stocks_response)} stocks returned")
        return stocks_response
    except Exception as e:
        log_error_with_exception("❌ Stock collection failed")
        return []
