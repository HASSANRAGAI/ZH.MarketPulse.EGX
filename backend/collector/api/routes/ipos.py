"""
IPO-related endpoints.
"""

from fastapi import HTTPException, BackgroundTasks
from typing import List
from datetime import datetime

from shared import logger, log_error_with_exception, get_session
from ...IPOCollector import ipo_collector
from data import responses


async def run_ipo_collection() -> int:
    """
    Run IPO data collection.

    Returns:
        Number of IPOs collected
    """
    try:
        logger.info("🔄 Running IPO collection")

        # Collect IPOs
        ipos_data = await ipo_collector.collect_ipos()

        # Save to database
        saved_count = await ipo_collector.save_ipos(ipos_data)

        logger.info(f"✅ IPO collection completed: {saved_count} records saved")
        return saved_count

    except Exception as e:
        log_error_with_exception("IPO collection failed")
        raise


async def collect_ipos(background_tasks: BackgroundTasks):
    """
    Trigger IPO data collection from Mubasher API.

    This endpoint starts the IPO collection process in the background
    and returns immediately with a status response.
    """
    try:
        logger.info("🚀 Starting IPO collection via API")

        # Run collection in background
        background_tasks.add_task(run_ipo_collection)

        return responses.StockCollectionResponse(  # Reuse the response model
            success=True,
            message="IPO collection started in background",
            timestamp=datetime.now()
        )

    except Exception as e:
        log_error_with_exception("Failed to start IPO collection")
        raise HTTPException(status_code=500, detail=f"Failed to start collection: {str(e)}")


async def collect_ipos_sync():
    """
    Trigger synchronous IPO data collection from Mubasher API.

    This endpoint waits for the collection to complete before returning.
    Use with caution as it may take several minutes.
    """
    try:
        logger.info("🚀 Starting synchronous IPO collection via API")

        # Run collection synchronously
        ipos_collected = await run_ipo_collection()

        return responses.StockCollectionResponse(
            success=True,
            message=f"IPO collection completed synchronously: {ipos_collected} records collected",
            timestamp=datetime.now()
        )

    except Exception as e:
        log_error_with_exception("Synchronous IPO collection failed")
        raise HTTPException(status_code=500, detail=f"Collection failed: {str(e)}")


async def get_ipos():
    """
    Retrieve all IPO records from the database.
    """
    try:
        logger.info("📊 Fetching IPOs from database")

        with get_session() as session:
            from data.models.ipo import IPO
            from data.models.stock import Stock
            from data.models.sector import Sector
            from data.models.market import Market
            from data.models.ipo_type import IPOType
            from data.models.ipo_status import IPOStatus

            result = session.execute(
                session.query(IPO, Stock, Sector.name.label('sector_en'), Sector.name_ar.label('sector_ar'), Market.name.label('market_en'), Market.name_ar.label('market_ar'), IPOType.name.label('type_en'), IPOType.name_ar.label('type_ar'), IPOStatus.name.label('status_en'), IPOStatus.name_ar.label('status_ar'))
                .join(Stock, IPO.stock_id == Stock.id, isouter=True)
                .join(Sector, IPO.sector_id == Sector.id, isouter=True)
                .join(Market, IPO.market_id == Market.id, isouter=True)
                .join(IPOType, IPO.type_id == IPOType.id, isouter=True)
                .join(IPOStatus, IPO.status_id == IPOStatus.id, isouter=True)
                .order_by(IPO.announced_at.desc())
            )

            ipos = []
            for ipo, stock, sector_en, sector_ar, market_en, market_ar, type_en, type_ar, status_en, status_ar in result:
                stock_base_data = {
                    'id': stock.id,
                    'symbol': stock.symbol,
                    'name': stock.name_en,
                    'name_ar': stock.name_ar,
                    'market': stock.market.name if stock and stock.market else None,
                    'sector': stock.sector.name if stock and stock.sector else None,
                    'currency': stock.currency
                } if stock else None

                ipos.append({
                    'id': ipo.id,
                    'name': ipo.name,
                    'name_ar': ipo.name_ar,
                    'url': ipo.url,
                    'status': status_en,
                    'status_ar': status_ar,
                    'attachment': ipo.attachment,
                    'type': type_en,
                    'type_ar': type_ar,
                    'market': market_en,
                    'market_ar': market_ar,
                    'sector': sector_en,
                    'sector_ar': sector_ar,
                    'market_url': None,  # Not stored, set to None
                    'volume': ipo.volume,
                    'announced_at': ipo.announced_at,
                    'stock_symbol': stock.symbol if stock else None,
                    'stock_name': stock.name_en if stock else None,
                    'stock_name_ar': stock.name_ar if stock else None,
                    'stock_base_data': stock_base_data
                })

        logger.info(f"✅ Retrieved {len(ipos)} IPO records")
        return ipos

    except Exception as e:
        log_error_with_exception("Failed to fetch IPOs")
        raise HTTPException(status_code=500, detail=f"Failed to fetch IPOs: {str(e)}")
