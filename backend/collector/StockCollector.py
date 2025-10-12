#!/usr/bin/env python3
"""
Stock Data Collector
Fetches stock information from Mubasher API endpoints.
"""

import asyncio
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

from shared import config_manager, logger, http_client, time_method, log_error_with_exception, get_session
from data import entities, StockResponse


class StockCollector:
    """
    Collects stock data from Mubasher API endpoints for both Arabic and English versions.
    """

    def __init__(self):
        self.config = config_manager.get('mubasher_endpoints', {})
        self.arabic_base = self.config.get('arabic_base', 'https://www.mubasher.info/')
        self.english_base = self.config.get('english_base', 'https://english.mubasher.info/')
        self.listed_companies_endpoint = self.config.get('listed_companies', 'api/1/listed-companies?country=eg&size={size}&start={start}')
        self.max_size = self.config.get('max_size', 30)
        self.request_delay = self.config.get('request_delay', 1.0)

    async def _fetch_stocks_arabic(self, page: int = 0, size: int = 0) -> Dict[str, Any]:
        """
        Fetch stock data from Arabic Mubasher endpoint.

        Args:
            page: Page number to fetch (0-based)
            size: Number of items to fetch per page

        Returns:
            JSON response from the API
        """
        if size <= 0:
            size = self.max_size

        url = f"{self.arabic_base}{self.listed_companies_endpoint.format(size=size, start=page * size)}"
        logger.info(f"🌐 Fetching Arabic stocks from: {url}")

        response = await http_client.get(url)
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Fetched {len(data.get('rows', []))} Arabic stocks from page {page}")
        return data

    async def _fetch_stocks_english(self, page: int = 0, size: int = 0) -> Dict[str, Any]:
        """
        Fetch stock data from English Mubasher endpoint.

        Args:
            page: Page number to fetch (0-based)

        Returns:
            JSON response from the API
        """
        if size <= 0:
            size = self.max_size

        url = f"{self.english_base}{self.listed_companies_endpoint.format(size=size, start=page * size)}"
        logger.info(f"🌐 Fetching English stocks from: {url}")

        response = await http_client.get(url)
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Fetched {len(data.get('rows', []))} English stocks from page {page}")
        return data

    def _merge_stock_data(self, ar_data: Dict[str, Any], en_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Merge Arabic and English stock data based on symbol.

        Args:
            ar_data: Arabic API response
            en_data: English API response

        Returns:
            List of merged stock dictionaries
        """
        merged_stocks = []

        # Create lookup dict for English data by symbol
        en_lookup = {stock['symbol']: stock for stock in en_data.get('rows', [])}

        for ar_stock in ar_data.get('rows', []):
            symbol = ar_stock['symbol']
            en_stock = en_lookup.get(symbol)

            if en_stock:
                # Merge data from both sources
                merged_stock = {
                    'symbol': symbol,
                    'name_en': en_stock.get('name', ''),
                    'name_ar': ar_stock.get('name', ''),
                    'sector_en': en_stock.get('sector', ''),
                    'sector_ar': ar_stock.get('sector', ''),
                    'market_en': en_stock.get('market', 'Egyptian Stock Exchange'),
                    'market_ar': ar_stock.get('market', 'البورصة المصرية'),
                    'currency': en_stock.get('currency') or ar_stock.get('currency') or 'EGP',
                    'profile_url': en_stock.get('profileUrl') or ar_stock.get('profileUrl'),
                    'current_price': en_stock.get('price'),
                    'change_percentage': en_stock.get('changePercentage'),
                    'last_update_str': en_stock.get('lastUpdate') or ar_stock.get('lastUpdate'),
                }
                merged_stocks.append(merged_stock)
            else:
                logger.warning(f"⚠️ No English data found for Arabic stock: {symbol}")

        return merged_stocks

    def _parse_last_update(self, last_update_str: str) -> Optional[datetime]:
        """
        Parse the last update string into a datetime object.

        Args:
            last_update_str: Date string from API (e.g., "23 September 2025" or "23 سبتمبر 2025")

        Returns:
            Parsed datetime or None if parsing fails
        """
        if not last_update_str:
            return None

        try:
            # Handle both English and Arabic date formats
            # For now, assume English format: "23 September 2025"
            # You might want to add Arabic date parsing logic here
            return datetime.strptime(last_update_str, '%d %B %Y')
        except ValueError:
            logger.warning(f"⚠️ Failed to parse date: {last_update_str}")
            return None

    async def collect_all_stocks(self) -> List[Dict[str, Any]]:
        """
        Collect all stocks from both Arabic and English endpoints.

        Returns:
            List of merged stock data dictionaries
        """
        logger.info("🚀 Starting stock collection from Mubasher API")

        all_stocks = []
        page = 0

        while True:
            try:
                # Fetch data from both endpoints concurrently
                ar_task = self._fetch_stocks_arabic(page, 600)
                en_task = self._fetch_stocks_english(page, 600)

                ar_data, en_data = await asyncio.gather(ar_task, en_task)

                # Merge the data
                page_stocks = self._merge_stock_data(ar_data, en_data)
                all_stocks.extend(page_stocks)

                # Check if we have more pages
                total_pages = max(
                    ar_data.get('numberOfPages', 1),
                    en_data.get('numberOfPages', 1)
                )

                logger.info(f"📄 Collected page {page + 1}/{total_pages} with {len(page_stocks)} stocks")

                if page + 1 >= total_pages:
                    break

                page += 1

                # Add delay between requests
                if self.request_delay > 0:
                    await asyncio.sleep(self.request_delay)

            except Exception as e:
                log_error_with_exception(f"❌ Error collecting stocks from page {page}")
                break

        logger.info(f"✅ Collected total of {len(all_stocks)} stocks")
        return all_stocks

    def save_stocks_to_db(self, stocks_data: List[Dict[str, Any]]) -> int:
        """
        Save stock data to the database.

        Args:
            stocks_data: List of stock data dictionaries

        Returns:
            Number of stocks saved/updated
        """
        saved_count = 0

        try:
            with get_session() as session:
                for stock_data in stocks_data:
                    try:
                        # Parse last update
                        last_update = self._parse_last_update(stock_data.get('last_update_str'))

                        # Check if stock already exists
                        existing_stock = session.query(entities.Stock).filter(entities.Stock.symbol == stock_data['symbol']).first()

                        # Get or create sector
                        sector_en = stock_data.get('sector_en')
                        sector_ar = stock_data.get('sector_ar')
                        sector = session.query(entities.Sector).filter(entities.Sector.name == sector_en).first()
                        if not sector:
                            sector = entities.Sector(name=sector_en, name_ar=sector_ar)
                            session.add(sector)
                            session.flush()  # Get the ID

                        # Get or create market
                        market_en = stock_data.get('market_en')
                        market_ar = stock_data.get('market_ar')
                        market = session.query(entities.Market).filter(entities.Market.name == market_en).first()
                        if not market:
                            market = entities.Market(name=market_en, name_ar=market_ar)
                            session.add(market)
                            session.flush()  # Get the ID

                        if existing_stock:
                            # Update existing stock
                            existing_stock.name_en = stock_data.get('name_en')
                            existing_stock.name_ar = stock_data.get('name_ar')
                            existing_stock.sector_id = sector.id
                            existing_stock.market_id = market.id
                            existing_stock.currency = stock_data.get('currency') or 'EGP'
                            existing_stock.profile_url = stock_data.get('profile_url')
                            existing_stock.current_price = stock_data.get('current_price')
                            existing_stock.change_percentage = stock_data.get('change_percentage')
                            existing_stock.last_update = last_update
                            existing_stock.is_active = True
                        else:
                            # Create new stock
                            new_stock = entities.Stock(
                                symbol=stock_data['symbol'],
                                name_en=stock_data.get('name_en'),
                                name_ar=stock_data.get('name_ar'),
                                sector_id=sector.id,
                                market_id=market.id,
                                currency=stock_data.get('currency') or 'EGP',
                                profile_url=stock_data.get('profile_url'),
                                current_price=stock_data.get('current_price'),
                                change_percentage=stock_data.get('change_percentage'),
                                last_update=last_update,
                                is_active=True
                            )
                            session.add(new_stock)

                        saved_count += 1

                    except Exception as e:
                        log_error_with_exception(f"❌ Error saving stock {stock_data.get('symbol')}")
                        continue

                session.commit()
                logger.info(f"💾 Saved/updated {saved_count} stocks in database")

        except Exception as e:
            log_error_with_exception("❌ Database error while saving stocks")
            raise

        return saved_count

    @time_method
    async def collect_and_save_stocks(self) -> int:
        """
        Collect stocks from API and save to database.

        Returns:
            Number of stocks saved/updated
        """
        logger.info("🎯 Starting complete stock collection and database update")

        # Collect data from API
        stocks_data = await self.collect_all_stocks()

        if not stocks_data:
            logger.warning("⚠️ No stock data collected")
            return 0

        # Save to database
        saved_count = self.save_stocks_to_db(stocks_data)

        logger.info(f"🎉 Stock collection completed: {saved_count} stocks processed")
        return saved_count

    @time_method
    async def get_stocks_db(self) -> List[StockResponse]:
        """
        Retrieve all active stocks from the database.

        Returns:
            List of Stock entities
        """
        try:
            with get_session() as session:
                stocks = session.query(entities.Stock).filter(entities.Stock.is_active == True).all()
                logger.info(f"📊 Retrieved {len(stocks)} active stocks from database")

                return [
                    StockResponse(
                        symbol=stock.symbol or "",
                        name_en=stock.name_en or "",
                        name_ar=stock.name_ar or "",
                        sector_en=stock.sector.name if stock.sector and stock.sector.name else "",
                        sector_ar=stock.sector.name_ar if stock.sector and stock.sector.name_ar else "",
                        market_en=stock.market.name if stock.market and stock.market.name else "",
                        market_ar=stock.market.name_ar if stock.market and stock.market.name_ar else "",
                        currency=stock.currency,
                        profile_url=stock.profile_url,
                        current_price=stock.current_price,
                        change_percentage=stock.change_percentage,
                        last_update=stock.last_update,
                        is_active=stock.is_active
                    )
                    for stock in stocks
                ]
        except Exception as e:
            log_error_with_exception("❌ Error retrieving stocks from database")
        return []

# Global collector instance
stock_collector = StockCollector()



async def run_get_stocks():
    """
    Get all collected stocks from the database.

    Returns:
        List of stock data
    """
    try:
        stocks_response = await stock_collector.get_stocks_db()
        logger.info(f"✅ Stock got from the Database: {len(stocks_response)} stocks returned")
        return stocks_response
    except Exception as e:
        log_error_with_exception("❌ Stock collection failed")
        return []


async def run_stock_collection() -> int:
    """
    Run the stock collection process.

    Returns:
        Number of stocks collected and saved
    """
    try:
        stocks_collected = await stock_collector.collect_and_save_stocks()
        logger.info(f"✅ Stock collection completed: {stocks_collected} stocks processed")
        return stocks_collected
    except Exception as e:
        log_error_with_exception("❌ Stock collection failed")
        return -1
