# browser_agent.py

import asyncio
from pyppeteer import launch
from utils.logger import logger

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/117.0.0.0 Safari/537.36"
)

class BrowserAgent:
    def __init__(self, headless=True, navigation_timeout=30000, retries=3, retry_delay=2):
        """
        Initializes the BrowserAgent.
        :param headless: Whether to launch browser in headless mode.
        :param navigation_timeout: Timeout for page navigation in milliseconds.
        :param retries: Number of retry attempts if navigation fails.
        :param retry_delay: Seconds to wait between retries (increases exponentially).
        """
        self.browser = None
        self.headless = headless
        self.navigation_timeout = navigation_timeout
        self.retries = retries
        self.retry_delay = retry_delay

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def start(self):
        """Launch the browser instance."""
        logger.info("[BrowserAgent] Launching headless browser...")
        try:
            self.browser = await launch(
                headless=self.headless,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--disable-dev-shm-usage",
                    "--disable-extensions"
                ],
                handleSIGINT=False,
                handleSIGTERM=False,
                handleSIGHUP=False
            )
            logger.info("[BrowserAgent] Browser launched successfully.")
        except Exception as e:
            logger.exception(f"[BrowserAgent] Failed to launch browser: {e}")
            raise RuntimeError("Browser launch failed.") from e

    async def navigate(self, url: str) -> str:
        """Navigate to a page and return its HTML content."""
        if not self.browser:
            raise RuntimeError("[BrowserAgent] Browser instance not initialized. Call start() first.")

        for attempt in range(1, self.retries + 1):
            try:
                logger.info(f"[BrowserAgent] Attempt {attempt}/{self.retries}: Navigating to {url}")
                page = await self.browser.newPage()

                # Setup headers
                await page.setUserAgent(DEFAULT_USER_AGENT)
                await page.setViewport({'width': 1280, 'height': 800})

                # Go to page
                await page.goto(url, timeout=self.navigation_timeout, waitUntil='networkidle2')
                await page.waitForSelector("body", timeout=5000)

                content = await page.content()
                await page.close()
                logger.info(f"[BrowserAgent] Navigation to {url} successful.")
                return content

            except Exception as e:
                logger.warning(f"[BrowserAgent] Attempt {attempt} failed: {e}")
                if attempt == self.retries:
                    logger.error(f"[BrowserAgent] All {self.retries} attempts to navigate {url} failed.")
                await asyncio.sleep(self.retry_delay * attempt)

        return ""

    async def close(self):
        """Close the browser instance safely."""
        if self.browser:
            try:
                await self.browser.close()
                logger.info("[BrowserAgent] Browser closed successfully.")
            except Exception as e:
                logger.warning(f"[BrowserAgent] Error closing browser: {e}")
        else:
            logger.debug("[BrowserAgent] No browser instance to close.")
