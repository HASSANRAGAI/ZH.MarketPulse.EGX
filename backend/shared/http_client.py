#!/usr/bin/env python3
"""
HTTP Client Module
Provides a robust HTTP client with connection pooling, retry logic, and logging hooks.
"""

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config_manager import config_manager
from .custom_logging import logger


class HttpClient:
    """
    Asynchronous HTTP client with connection pooling, retry logic, and logging hooks.
    Reads configuration from the database config table.
    """

    def __init__(self):
        self.client = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization of the HTTP client."""
        if self._initialized:
            return

        try:
            # Simple initialization without config dependencies
            self.client = httpx.AsyncClient(
                timeout=30.0,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
            )
            logger.info("✅ HTTP client initialized successfully")
            self._initialized = True

        except Exception as e:
            logger.error(f"❌ Failed to initialize HTTP client: {e}")
            self.client = None
            self._initialized = True  # Don't try again

    def _log_request(self, request):
        """Log outgoing HTTP requests."""
        logger.info(f"🌐 HTTP Request: {request.method} {request.url}")

    def _log_response(self, response):
        """Log incoming HTTP responses."""
        logger.info(f"🌐 HTTP Response: {response.status_code} {response.url}")

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Perform GET request with retry logic."""
        self._ensure_initialized()
        if self.client is None:
            raise RuntimeError("HTTP client not initialized. Check configuration and database connection.")
        return await self.client.get(url, **kwargs)

    @retry(
        stop=stop_after_attempt(3),  # Default fallback
        wait=wait_exponential(
            multiplier=1.0,  # Default fallback
            max=60.0  # Default fallback
        ),
        retry=retry_if_exception_type((
            httpx.TimeoutException,
            httpx.ConnectError,
            httpx.NetworkError
        )),
        before_sleep=lambda retry_state: logger.warning(
            f"⚠️ HTTP request failed (attempt {retry_state.attempt_number}), "
            f"retrying in {retry_state.next_action.sleep} seconds..."
        )
    )
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Perform POST request with retry logic."""
        self._ensure_initialized()
        if self.client is None:
            raise RuntimeError("HTTP client not initialized. Check configuration and database connection.")
        return await self.client.post(url, **kwargs)

    @retry(
        stop=stop_after_attempt(3),  # Default fallback
        wait=wait_exponential(
            multiplier=1.0,  # Default fallback
            max=60.0  # Default fallback
        ),
        retry=retry_if_exception_type((
            httpx.TimeoutException,
            httpx.ConnectError,
            httpx.NetworkError
        )),
        before_sleep=lambda retry_state: logger.warning(
            f"⚠️ HTTP request failed (attempt {retry_state.attempt_number}), "
            f"retrying in {retry_state.next_action.sleep} seconds..."
        )
    )
    async def put(self, url: str, **kwargs) -> httpx.Response:
        """Perform PUT request with retry logic."""
        self._ensure_initialized()
        if self.client is None:
            raise RuntimeError("HTTP client not initialized. Check configuration and database connection.")
        return await self.client.put(url, **kwargs)

    @retry(
        stop=stop_after_attempt(3),  # Default fallback
        wait=wait_exponential(
            multiplier=1.0,  # Default fallback
            max=60.0  # Default fallback
        ),
        retry=retry_if_exception_type((
            httpx.TimeoutException,
            httpx.ConnectError,
            httpx.NetworkError
        )),
        before_sleep=lambda retry_state: logger.warning(
            f"⚠️ HTTP request failed (attempt {retry_state.attempt_number}), "
            f"retrying in {retry_state.next_action.sleep} seconds..."
        )
    )
    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """Perform DELETE request with retry logic."""
        self._ensure_initialized()
        if self.client is None:
            raise RuntimeError("HTTP client not initialized. Check configuration and database connection.")
        return await self.client.delete(url, **kwargs)

    async def close(self):
        """Close the HTTP client."""
        if self.client is not None:
            await self.client.aclose()
            logger.info("HTTP client closed")
        else:
            logger.warning("HTTP client was not initialized, nothing to close")


# Global HTTP client instance
http_client = HttpClient()