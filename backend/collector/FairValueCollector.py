#!/usr/bin/env python3
"""
Fair Value Data Collector
Fetches fair value recommendations from Mubasher API endpoints.
"""

import asyncio
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

from shared import config_manager, logger, http_client, time_method, log_error_with_exception, get_session
from data.models.fair_value import FairValue
from data.models.stock import Stock
from data.models.source import Source
from data.models.recommendation import Recommendation
from data.models.source_type import SourceType


class FairValueCollector:
    """
    Collects fair value recommendation data from Mubasher API endpoints for both Arabic and English versions.
    """

    def __init__(self):
        self.config = config_manager.get('mubasher_endpoints', {})
        self.arabic_base = self.config.get('arabic_base', 'https://www.mubasher.info/')
        self.english_base = self.config.get('english_base', 'https://english.mubasher.info/')
        self.fair_values_endpoint = self.config.get('fairValues', 'api/1/fairValues?country=eg&size={size}&start={start}')
        self.max_size = self.config.get('max_size', 30)
        self.request_delay = self.config.get('request_delay', 5.0)

    async def _fetch_fair_values_arabic(self, page: int = 0, size: int = 0) -> Dict[str, Any]:
        """
        Fetch fair value data from Arabic Mubasher endpoint.

        Args:
            page: Page number to fetch (0-based)
            size: Number of items to fetch per page

        Returns:
            JSON response from the API
        """
        if size <= 0:
            size = self.max_size

        url = f"{self.arabic_base}{self.fair_values_endpoint.format(size=size, start=page * size)}"
        logger.info(f"🌐 Fetching Arabic fair values from: {url}")

        response = await http_client.get(url)
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Fetched {len(data.get('rows', []))} Arabic fair values from page {page}")
        return data

    async def _fetch_fair_values_english(self, page: int = 0, size: int = 0) -> Dict[str, Any]:
        """
        Fetch fair value data from English Mubasher endpoint.

        Args:
            page: Page number to fetch (0-based)
            size: Number of items to fetch per page

        Returns:
            JSON response from the API
        """
        if size <= 0:
            size = self.max_size

        url = f"{self.english_base}{self.fair_values_endpoint.format(size=size, start=page * size)}"
        logger.info(f"🌐 Fetching English fair values from: {url}")

        response = await http_client.get(url)
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Fetched {len(data.get('rows', []))} English fair values from page {page}")
        return data

    def _extract_symbol_from_url(self, url: str) -> Optional[str]:
        """
        Extract stock symbol from Mubasher URL.

        Args:
            url: Mubasher stock URL

        Returns:
            Stock symbol or None if not found
        """
        if not url:
            return None
        # URL format: /markets/EGX/stocks/SYMBOL
        parts = url.strip('/').split('/')
        if len(parts) >= 4 and parts[0] == 'markets' and parts[1] == 'EGX' and parts[2] == 'stocks':
            return parts[3]
        return None

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string from Mubasher API.

        Args:
            date_str: Date string like "14 February 2019" or "01 سبتمبر 2025"

        Returns:
            Parsed datetime or None
        """
        if not date_str:
            return None

        # Dictionary to translate Arabic month names to English
        arabic_months = {
            'يناير': 'January',
            'فبراير': 'February',
            'مارس': 'March',
            'أبريل': 'April',
            'مايو': 'May',
            'يونيو': 'June',
            'يوليو': 'July',
            'أغسطس': 'August',
            'سبتمبر': 'September',
            'أكتوبر': 'October',
            'نوفمبر': 'November',
            'ديسمبر': 'December'
        }

        try:
            # Split the date string
            parts = date_str.split()
            if len(parts) != 3:
                raise ValueError("Invalid date format")

            day, month, year = parts

            # Translate month if it's Arabic
            if month in arabic_months:
                month = arabic_months[month]

            # Reconstruct the date string in English
            english_date_str = f"{day} {month} {year}"

            # Parse the English date
            return datetime.strptime(english_date_str, '%d %B %Y')

        except (ValueError, KeyError) as e:
            logger.warning(f"Could not parse date: {date_str} - {e}")
            return None

    async def collect_fair_values(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Collect fair value data from both Arabic and English endpoints.

        Args:
            max_pages: Maximum number of pages to fetch (None for all)

        Returns:
            List of collected fair value data
        """
        # Get the max released_at from the database
        max_released_at = await self._get_max_released_at()
        logger.info(f"📅 Max released_at in DB: {max_released_at}")

        collected_data = []

        # Fetch from English endpoint first (primary)
        english_data = await self._collect_from_endpoint(
            self._fetch_fair_values_english, max_pages, "English"
        )
        collected_data.extend(english_data)

        # Fetch from Arabic endpoint
        arabic_data = await self._collect_from_endpoint(
            self._fetch_fair_values_arabic, max_pages, "Arabic"
        )
        collected_data.extend(arabic_data)

        # Filter to only new data since max_released_at
        if max_released_at:
            filtered_data = [data for data in collected_data if data['released_at'] and data['released_at'] > max_released_at]
            logger.info(f"🔄 Filtered {len(collected_data)} to {len(filtered_data)} new fair values since {max_released_at}")
            collected_data = filtered_data
        else:
            logger.info(f"🔄 No max released_at found, processing all {len(collected_data)} fair values")

        logger.info(f"🎉 Collected total {len(collected_data)} new fair value records")
        return collected_data

    async def _collect_from_endpoint(self, fetch_func, max_pages: Optional[int], language: str) -> List[Dict[str, Any]]:
        """
        Collect data from a specific endpoint.

        Args:
            fetch_func: Function to fetch data
            max_pages: Max pages to fetch
            language: Language for logging

        Returns:
            List of collected data
        """
        data = []
        page = 0

        while max_pages is None or page < max_pages:
            try:
                response = await fetch_func(page, self.max_size)
                rows = response.get('rows', [])

                if not rows:
                    break

                for row in rows:
                    processed_row = self._process_fair_value_row(row, language == "Arabic")
                    if processed_row:
                        data.append(processed_row)

                number_of_pages = response.get('numberOfPages', 1)
                if page + 1 >= number_of_pages:
                    break

                page += 1
                await asyncio.sleep(self.request_delay)

            except Exception as e:
                logger.error(f"❌ Error fetching {language} fair values page {page}: {e}")
                break

        return data

    def _process_fair_value_row(self, row: Dict[str, Any], is_arabic: bool = False) -> Optional[Dict[str, Any]]:
        """
        Process a single fair value row from the API.

        Args:
            row: Raw row data from API
            is_arabic: Whether the data is from Arabic endpoint

        Returns:
            Processed row data or None if invalid
        """
        try:
            symbol = self._extract_symbol_from_url(row.get('url', ''))
            if not symbol:
                logger.warning(f"Could not extract symbol from URL: {row.get('url')}")
                return None

            released_at = self._parse_date(row.get('releasedAt', ''))

            processed = {
                'symbol': symbol,
                'released_at': released_at,
                'source_name': row.get('source') if not is_arabic else None,
                'source_name_ar': row.get('source') if is_arabic else None,
                'recommendation_name': row.get('recommendation') if not is_arabic else None,
                'recommendation_name_ar': row.get('recommendation') if is_arabic else None,
                'value': row.get('value'),
                'price': row.get('price'),
                'last_price': row.get('lastPrice'),
                'change': row.get('change'),
                'change_percentage': row.get('changePercentage')
            }

            return processed

        except Exception as e:
            logger.error(f"❌ Error processing fair value row: {e}")
            return None

    async def _get_max_released_at(self) -> Optional[datetime]:
        """
        Get the maximum released_at date from the database.

        Returns:
            Max released_at or None
        """
        with get_session() as session:
            result = session.execute(
                session.query(FairValue.released_at).order_by(FairValue.released_at.desc()).limit(1)
            ).scalar_one_or_none()
            return result

    @time_method
    async def save_fair_values(self, fair_values_data: List[Dict[str, Any]]) -> int:
        """
        Save fair value data to the database.

        Args:
            fair_values_data: List of fair value data to save

        Returns:
            Number of records saved
        """
        saved_count = 0

        with get_session() as session:
            try:
                for data in fair_values_data:
                    # Find the stock by symbol
                    stock = session.execute(
                        session.query(Stock).filter(Stock.symbol == data['symbol'])
                    ).scalar_one_or_none()

                    if not stock:
                        logger.warning(f"Stock not found for symbol: {data['symbol']}")
                        continue

                    # Get or create source
                    source_name = data['source_name']
                    source_name_ar = data['source_name_ar']
                    if source_name:
                        source = session.execute(
                            session.query(Source).filter(Source.name == source_name)
                        ).scalar_one_or_none()
                        if not source:
                            # Get the default source type (financial services companies)
                            source_type = session.execute(
                                session.query(SourceType).filter(SourceType.name == 'financial services companies')
                            ).scalar_one_or_none()
                            if not source_type:
                                # Create it if not exists
                                source_type = SourceType(name='financial services companies', name_ar='شركات خدمات مالية')
                                session.add(source_type)
                                session.flush()  # To get id
                            source = Source(name=source_name, name_ar=source_name_ar, type_id=source_type.id)
                            session.add(source)
                            session.flush()
                        source_id = source.id
                    else:
                        source_id = None

                    # Get or create recommendation
                    recommendation_name = data['recommendation_name']
                    recommendation_name_ar = data['recommendation_name_ar']
                    if recommendation_name:
                        recommendation = session.execute(
                            session.query(Recommendation).filter(Recommendation.name == recommendation_name)
                        ).scalar_one_or_none()
                        if not recommendation:
                            recommendation = Recommendation(name=recommendation_name, name_ar=recommendation_name_ar)
                            session.add(recommendation)
                            session.flush()
                        recommendation_id = recommendation.id
                    else:
                        recommendation_id = None

                    # Check if fair value already exists (by stock_id, released_at, source_id)
                    existing = session.execute(
                        session.query(FairValue).filter(
                            FairValue.stock_id == stock.id,
                            FairValue.released_at == data['released_at'],
                            FairValue.source_id == source_id
                        )
                    ).scalar_one_or_none()

                    if existing:
                        # Update existing
                        existing.recommendation_id = recommendation_id
                        existing.value = data['value']
                        existing.price = data['price']
                        existing.last_price = data['last_price']
                        existing.change = data['change']
                        existing.change_percentage = data['change_percentage']
                    else:
                        # Create new
                        fair_value = FairValue(
                            stock_id=stock.id,
                            released_at=data['released_at'],
                            source_id=source_id,
                            recommendation_id=recommendation_id,
                            value=data['value'],
                            price=data['price'],
                            last_price=data['last_price'],
                            change=data['change'],
                            change_percentage=data['change_percentage']
                        )
                        session.add(fair_value)

                    saved_count += 1

                session.commit()
                logger.info(f"💾 Saved {saved_count} fair value records to database")

            except Exception as e:
                session.rollback()
                logger.error(f"❌ Error saving fair values: {e}")
                raise

        return saved_count


# Global instance
fair_value_collector = FairValueCollector()
