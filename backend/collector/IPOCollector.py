#!/usr/bin/env python3
"""
IPO Data Collector
Fetches IPO data from Mubasher API endpoints.
"""

import asyncio
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

from shared import config_manager, logger, http_client, time_method, log_error_with_exception, get_session
from data.models.ipo import IPO
from data.models.ipo_status import IPOStatus
from data.models.ipo_type import IPOType
from data.models.sector import Sector
from data.models.market import Market
from data.models.stock import Stock


class IPOCollector:
    """
    Collects IPO data from Mubasher API endpoints for both Arabic and English versions.
    """

    def __init__(self):
        self.config = config_manager.get('mubasher_endpoints', {})
        self.arabic_base = self.config.get('arabic_base', 'https://www.mubasher.info/')
        self.english_base = self.config.get('english_base', 'https://english.mubasher.info/')
        self.ipos_endpoint = self.config.get('ipos', 'api/1/ipos?country=eg&size={size}&start={start}')
        self.max_size = self.config.get('max_size', 30)
        self.request_delay = self.config.get('request_delay', 1.0)

    async def _fetch_ipos_arabic(self, page: int = 0, size: int = 0) -> Dict[str, Any]:
        """
        Fetch IPO data from Arabic Mubasher endpoint.

        Args:
            page: Page number to fetch (0-based)
            size: Number of items to fetch per page

        Returns:
            JSON response from the API
        """
        if size <= 0:
            size = self.max_size

        url = f"{self.arabic_base}{self.ipos_endpoint.format(size=size, start=page * size)}"
        logger.info(f"🌐 Fetching Arabic IPOs from: {url}")

        response = await http_client.get(url)
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Fetched {len(data.get('rows', []))} Arabic IPOs from page {page}")
        return data

    async def _fetch_ipos_english(self, page: int = 0, size: int = 0) -> Dict[str, Any]:
        """
        Fetch IPO data from English Mubasher endpoint.

        Args:
            page: Page number to fetch (0-based)
            size: Number of items to fetch per page

        Returns:
            JSON response from the API
        """
        if size <= 0:
            size = self.max_size

        url = f"{self.english_base}{self.ipos_endpoint.format(size=size, start=page * size)}"
        logger.info(f"🌐 Fetching English IPOs from: {url}")

        response = await http_client.get(url)
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Fetched {len(data.get('rows', []))} English IPOs from page {page}")
        return data

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string from Mubasher API.

        Args:
            date_str: Date string like "09 February 2023" or "09 فبراير 2023"

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

    async def collect_ipos(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Collect IPO data from both Arabic and English endpoints.

        Args:
            max_pages: Maximum number of pages to fetch (None for all)

        Returns:
            List of collected IPO data
        """
        collected_data = []

        # Fetch from English endpoint first (primary)
        english_data = await self._collect_from_endpoint(
            self._fetch_ipos_english, max_pages, "English"
        )
        collected_data.extend(english_data)

        # Fetch from Arabic endpoint
        arabic_data = await self._collect_from_endpoint(
            self._fetch_ipos_arabic, max_pages, "Arabic"
        )
        collected_data.extend(arabic_data)

        logger.info(f"🎉 Collected total {len(collected_data)} IPO records")
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
                    processed_row = self._process_ipo_row(row, language == "Arabic")
                    if processed_row:
                        data.append(processed_row)

                number_of_pages = response.get('numberOfPages', 1)
                if page + 1 >= number_of_pages:
                    break

                page += 1
                await asyncio.sleep(self.request_delay)

            except Exception as e:
                logger.error(f"❌ Error fetching {language} IPOs page {page}: {e}")
                break

        return data

    def _process_ipo_row(self, row: Dict[str, Any], is_arabic: bool = False) -> Optional[Dict[str, Any]]:
        """
        Process a single IPO row from the API.

        Args:
            row: Raw row data from API
            is_arabic: Whether the data is from Arabic endpoint

        Returns:
            Processed row data or None if invalid
        """
        try:
            announced_at = self._parse_date(row.get('announcedAt', ''))

            processed = {
                'name': row.get('name') if not is_arabic else None,
                'name_ar': row.get('name') if is_arabic else None,
                'url': row.get('url'),
                'status': row.get('status') if not is_arabic else None,
                'status_ar': row.get('status') if is_arabic else None,
                'attachment': row.get('attachment'),
                'type': row.get('type') if not is_arabic else None,
                'type_ar': row.get('type') if is_arabic else None,
                'market': row.get('market') if not is_arabic else None,
                'market_ar': row.get('market') if is_arabic else None,
                'sector': row.get('sector') if not is_arabic else None,
                'sector_ar': row.get('sector') if is_arabic else None,
                'volume': row.get('volume'),
                'announced_at': announced_at
            }

            return processed

        except Exception as e:
            logger.error(f"❌ Error processing IPO row: {e}")
            return None

    @time_method
    async def save_ipos(self, ipos_data: List[Dict[str, Any]]) -> int:
        """
        Save IPO data to the database.

        Args:
            ipos_data: List of IPO data to save

        Returns:
            Number of records saved
        """
        saved_count = 0

        with get_session() as session:
            try:
                for data in ipos_data:
                    # Get or create related entities
                    status_name = data.get('status')
                    status_ar = data.get('status_ar')
                    if status_name:
                        ipo_status = session.query(IPOStatus).filter(IPOStatus.name == status_name).first()
                        if not ipo_status:
                            ipo_status = IPOStatus(name=status_name, name_ar=status_ar)
                            session.add(ipo_status)
                            session.flush()
                        status_id = ipo_status.id
                    else:
                        status_id = None

                    type_name = data.get('type')
                    type_ar = data.get('type_ar')
                    if type_name:
                        ipo_type = session.query(IPOType).filter(IPOType.name == type_name).first()
                        if not ipo_type:
                            ipo_type = IPOType(name=type_name, name_ar=type_ar)
                            session.add(ipo_type)
                            session.flush()
                        type_id = ipo_type.id
                    else:
                        type_id = None

                    market_name = data.get('market')
                    market_ar = data.get('market_ar')
                    if market_name:
                        market = session.query(Market).filter(Market.name == market_name).first()
                        if not market:
                            market = Market(name=market_name, name_ar=market_ar)
                            session.add(market)
                            session.flush()
                        market_id = market.id
                    else:
                        market_id = None

                    sector_name = data.get('sector')
                    sector_ar = data.get('sector_ar')
                    if sector_name:
                        sector = session.query(Sector).filter(Sector.name == sector_name).first()
                        if not sector:
                            sector = Sector(name=sector_name, name_ar=sector_ar)
                            session.add(sector)
                            session.flush()
                        sector_id = sector.id
                    else:
                        sector_id = None

                    # Extract stock symbol from URL if matches pattern
                    stock_id = None
                    url = data.get('url')
                    if url:
                        parsed = urlparse(url)
                        path_parts = parsed.path.strip('/').split('/')
                        try:
                            stocks_index = path_parts.index('stocks')
                            if stocks_index + 1 < len(path_parts):
                                stock_symbol = path_parts[stocks_index + 1]
                                stock = session.query(Stock).filter(Stock.symbol == stock_symbol).first()
                                if stock:
                                    stock_id = stock.id
                        except ValueError:
                            pass

                    # Get or create IPO based on name and announced_at
                    name = data['name']
                    announced_at = data['announced_at']

                    if name and announced_at:
                        existing = session.query(IPO).filter(
                            IPO.name == name,
                            IPO.announced_at == announced_at
                        ).first()

                        if existing:
                            # Update existing
                            existing.name_ar = data['name_ar']
                            existing.url = data['url']
                            existing.status_id = status_id
                            existing.attachment = data['attachment']
                            existing.type_id = type_id
                            existing.market_id = market_id
                            existing.sector_id = sector_id
                            existing.volume = data['volume']
                            existing.stock_id = stock_id
                        else:
                            # Create new
                            ipo = IPO(
                                name=name,
                                name_ar=data['name_ar'],
                                url=data['url'],
                                status_id=status_id,
                                attachment=data['attachment'],
                                type_id=type_id,
                                market_id=market_id,
                                sector_id=sector_id,
                                volume=data['volume'],
                                announced_at=announced_at,
                                stock_id=stock_id
                            )
                            session.add(ipo)

                        saved_count += 1

                session.commit()
                logger.info(f"💾 Saved {saved_count} IPO records to database")

            except Exception as e:
                session.rollback()
                logger.error(f"❌ Error saving IPOs: {e}")
                raise

        return saved_count


# Global instance
ipo_collector = IPOCollector()
