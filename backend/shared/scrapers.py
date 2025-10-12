#!/usr/bin/env python3
"""
Web Scraping Module
Provides web scraping functionality using Selenium, ChromeDriver, and BeautifulSoup.

Requirements:
- ChromeDriver must be installed and available in PATH, or set chrome_driver_path in config
- Chrome browser must be installed on the system

Configuration:
- Uses chrome_options from default_config.json for Chrome settings
- Uses scraping.request_timeout for timeouts
- Set scraper.chrome_driver_path if ChromeDriver is not in PATH
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import asyncio
from typing import Optional, Dict, Any
import time

from .config_manager import config_manager
from .custom_logging import logger, log_error_with_exception
from .retry import smart_retry


class WebScraper:
    """
    Web scraper using Selenium with ChromeDriver and BeautifulSoup for parsing.
    Reads configuration from the database config table.

    Usage:
        from shared import web_scraper

        # Using context manager (recommended)
        with web_scraper:
            soup = web_scraper.load_page('https://example.com')
            title = soup.find('h1').text

        # Manual control
        web_scraper.start_driver()
        try:
            soup = web_scraper.load_page('https://example.com', wait_selector='h1')
            links = web_scraper.find_elements('a')
        finally:
            web_scraper.stop_driver()
    """

    def __init__(self):
        # Read scraper configuration from database
        chrome_config = config_manager.get('chrome_options', {})
        self.headless = chrome_config.get('headless', True)
        self.window_size = chrome_config.get('window_size', '1920,1080')
        self.user_agent = chrome_config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        # Additional scraper-specific configs
        self.page_load_timeout = config_manager.get('scraping.request_timeout', 30)
        self.implicit_wait = config_manager.get('scraping.request_timeout', 10)  # Use same as page_load_timeout
        self.chrome_path = config_manager.get('scraper.chrome_driver_path', None)

        self.driver: Optional[webdriver.Chrome] = None

    def _setup_chrome_options(self) -> Options:
        """Configure Chrome options for scraping."""
        options = Options()

        chrome_config = config_manager.get('chrome_options', {})

        if chrome_config.get('headless', True):
            options.add_argument('--headless')

        options.add_argument(f'--window-size={chrome_config.get("window_size", "1920,1080")}')
        options.add_argument(f'--user-agent={chrome_config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")}')

        if chrome_config.get('no_sandbox', True):
            options.add_argument('--no-sandbox')

        if chrome_config.get('disable_dev_shm_usage', True):
            options.add_argument('--disable-dev-shm-usage')

        if chrome_config.get('disable_gpu', True):
            options.add_argument('--disable-gpu')

        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Speed up loading
        options.add_argument('--disable-javascript')  # Optional: disable JS for faster loading
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')

        # Additional options for better scraping
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')

        return options

    def _create_driver(self) -> webdriver.Chrome:
        """Create and configure Chrome WebDriver."""
        options = self._setup_chrome_options()

        service = Service(self.chrome_path) if self.chrome_path else Service()

        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.implicitly_wait(self.implicit_wait)
        driver.set_page_load_timeout(self.page_load_timeout)

        return driver

    def start_driver(self):
        """Start the Chrome WebDriver."""
        if self.driver is None:
            try:
                self.driver = self._create_driver()
                logger.info("🚀 Chrome WebDriver started successfully")
            except Exception as e:
                log_error_with_exception("❌ Failed to start Chrome WebDriver")
                raise

    def stop_driver(self):
        """Stop the Chrome WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("🛑 Chrome WebDriver stopped")
            except Exception as e:
                logger.warning(f"⚠️ Error stopping WebDriver: {e}")
            finally:
                self.driver = None

    @smart_retry("page_load")
    def load_page(self, url: str, wait_selector: Optional[str] = None) -> BeautifulSoup:
        """
        Load a webpage and return BeautifulSoup object.

        Args:
            url: URL to load
            wait_selector: CSS selector to wait for before returning

        Returns:
            BeautifulSoup object of the page content
        """
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call start_driver() first.")

        try:
            logger.info(f"🌐 Loading page: {url}")
            self.driver.get(url)

            if wait_selector:
                WebDriverWait(self.driver, self.page_load_timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
                )
                logger.info(f"✅ Waited for selector: {wait_selector}")

            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            logger.info(f"✅ Page loaded successfully: {url}")
            return soup

        except TimeoutException:
            log_error_with_exception(f"⏰ Timeout loading page: {url}")
            raise
        except WebDriverException as e:
            log_error_with_exception(f"🌐 WebDriver error loading page {url}")
            raise
        except Exception as e:
            log_error_with_exception(f"❌ Unexpected error loading page {url}")
            raise

    def find_element(self, selector: str, by: By = By.CSS_SELECTOR) -> Optional[Any]:
        """
        Find a single element on the current page.

        Args:
            selector: Selector to find
            by: Selenium By method

        Returns:
            WebElement or None if not found
        """
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call start_driver() first.")

        try:
            element = self.driver.find_element(by, selector)
            return element
        except Exception as e:
            logger.warning(f"⚠️ Element not found: {selector} - {e}")
            return None

    def find_elements(self, selector: str, by: By = By.CSS_SELECTOR) -> list:
        """
        Find multiple elements on the current page.

        Args:
            selector: Selector to find
            by: Selenium By method

        Returns:
            List of WebElements
        """
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call start_driver() first.")

        try:
            elements = self.driver.find_elements(by, selector)
            return elements
        except Exception as e:
            logger.warning(f"⚠️ Elements not found: {selector} - {e}")
            return []

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript on the current page.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Result of script execution
        """
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call start_driver() first.")

        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            log_error_with_exception("❌ JavaScript execution failed")
            raise

    def take_screenshot(self, filename: str) -> bool:
        """
        Take a screenshot of the current page.

        Args:
            filename: Path to save the screenshot

        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call start_driver() first.")

        try:
            self.driver.save_screenshot(filename)
            logger.info(f"📸 Screenshot saved: {filename}")
            return True
        except Exception as e:
            log_error_with_exception("❌ Failed to take screenshot")
            return False

    async def scrape_async(self, url: str, wait_selector: Optional[str] = None) -> BeautifulSoup:
        """
        Async wrapper for page loading (since Selenium is synchronous).
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.load_page, url, wait_selector)

    def __enter__(self):
        """Context manager entry."""
        self.start_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_driver()


# Global scraper instance
web_scraper = WebScraper()