import requests
from bs4 import BeautifulSoup
import time
import logging
import urllib.parse

class WebSearcher:
    def __init__(self, base_url="https://html.duckduckgo.com/html/", headers=None):
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        # Setup logger only if not already configured
        self.logger = logging.getLogger("WebSearcher")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def search(self, query, max_results=5, retries=3, pause=2):
        """
        Perform a search on DuckDuckGo and return the results.

        :param query: The search query.
        :param max_results: Number of results to return.
        :param retries: Retry attempts on failure.
        :param pause: Pause between retries (seconds).
        :return: List of dicts with 'title' and 'link'.
        """
        encoded_query = urllib.parse.quote_plus(query)
        url = f"{self.base_url}?q={encoded_query}"

        for attempt in range(1, retries + 1):
            try:
                self.logger.info(f"[Search Attempt {attempt}] Query: {query}")
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                return self._parse_results(soup, max_results)

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Search error: {e}")
                time.sleep(pause * attempt)  # Exponential backoff

        self.logger.error("All retries failed.")
        return []

    def _parse_results(self, soup, max_results):
        """
        Extracts links and titles from DuckDuckGo HTML result page.
        :param soup: Parsed HTML from BeautifulSoup.
        :param max_results: Limit number of results.
        :return: List of {'title': ..., 'link': ...}
        """
        results = []
        links = soup.find_all("a", class_="result__a", limit=max_results)

        for tag in links:
            title = tag.get_text(strip=True)
            href = tag.get("href")

            if href and title:
                results.append({
                    "title": title,
                    "link": href
                })

        self.logger.info(f"Extracted {len(results)} result(s)")
        return results
