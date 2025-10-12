"""
Fair value-related endpoints.
"""

from fastapi import HTTPException, BackgroundTasks
from typing import List
from datetime import datetime

from shared import logger, log_error_with_exception, get_session
from ...FairValueCollector import fair_value_collector
from data import responses


async def run_fair_value_collection() -> int:
    """
    Run fair value data collection.

    Returns:
        Number of fair values collected
    """
    try:
        logger.info("🔄 Running fair value collection")

        # Collect fair values
        fair_values_data = await fair_value_collector.collect_fair_values()

        # Save to database
        saved_count = await fair_value_collector.save_fair_values(fair_values_data)

        logger.info(f"✅ Fair value collection completed: {saved_count} records saved")
        return saved_count

    except Exception as e:
        log_error_with_exception("Fair value collection failed")
        raise


async def collect_fair_values(background_tasks: BackgroundTasks):
    """
    Trigger fair value data collection from Mubasher API.

    This endpoint starts the fair value collection process in the background
    and returns immediately with a status response.
    """
    try:
        logger.info("🚀 Starting fair value collection via API")

        # Run collection in background
        background_tasks.add_task(run_fair_value_collection)

        return responses.StockCollectionResponse(  # Reuse the response model
            success=True,
            message="Fair value collection started in background",
            timestamp=datetime.now()
        )

    except Exception as e:
        log_error_with_exception("Failed to start fair value collection")
        raise HTTPException(status_code=500, detail=f"Failed to start collection: {str(e)}")


async def collect_fair_values_sync():
    """
    Trigger synchronous fair value data collection from Mubasher API.

    This endpoint waits for the collection to complete before returning.
    Use with caution as it may take several minutes.
    """
    try:
        logger.info("🚀 Starting synchronous fair value collection via API")

        # Run collection synchronously
        fair_values_collected = await run_fair_value_collection()

        return responses.StockCollectionResponse(
            success=True,
            message=f"Fair value collection completed synchronously: {fair_values_collected} records collected",
            timestamp=datetime.now()
        )

    except Exception as e:
        log_error_with_exception("Synchronous fair value collection failed")
        raise HTTPException(status_code=500, detail=f"Collection failed: {str(e)}")


async def get_fair_values():
    """
    Retrieve all fair value records from the database.
    """
    try:
        logger.info("📊 Fetching fair values from database")

        with get_session() as session:
            from data.models.fair_value import FairValue
            from data.models.stock import Stock
            from data.models.source import Source
            from data.models.recommendation import Recommendation
            from data.models.sector import Sector
            from data.models.market import Market

            result = session.execute(
                session.query(FairValue, Stock.symbol, Market.name.label('market_en'), Sector.name.label('sector_en'), Source.name.label('source_name'), Source.name_ar.label('source_name_ar'), Recommendation.name.label('recommendation_name'), Recommendation.name_ar.label('recommendation_name_ar'))
                .join(Stock, FairValue.stock_id == Stock.id)
                .join(Market, Stock.market_id == Market.id)
                .join(Sector, Stock.sector_id == Sector.id)
                .join(Source, FairValue.source_id == Source.id)
                .join(Recommendation, FairValue.recommendation_id == Recommendation.id)
                .order_by(FairValue.released_at.desc())
            )

            fair_values = []
            for fv, symbol, market_en, sector_en, source_name, source_name_ar, recommendation_name, recommendation_name_ar in result:
                fair_values.append({
                    'id': fv.id,
                    'symbol': symbol,
                    'released_at': fv.released_at,
                    'source': source_name,
                    'source_ar': source_name_ar,
                    'recommendation': recommendation_name,
                    'recommendation_ar': recommendation_name_ar,
                    'market': market_en,
                    'sector': sector_en,
                    'market_url': None,  # Not stored, set to None
                    'value': fv.value,
                    'price': fv.price,
                    'last_price': fv.last_price,
                    'change': fv.change,
                    'change_percentage': fv.change_percentage
                })

        logger.info(f"✅ Retrieved {len(fair_values)} fair value records")
        return fair_values

    except Exception as e:
        log_error_with_exception("Failed to fetch fair values")
        raise HTTPException(status_code=500, detail=f"Failed to fetch fair values: {str(e)}")
