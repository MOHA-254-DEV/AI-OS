# dropship_agent.py

import requests
import json
import os
import re
from bs4 import BeautifulSoup
from typing import List, Dict
from utils.logger import log_task
from agents.ai_writer import AIWriter

class DropshipAgent:
    def __init__(self, save_path: str = "data/dropship/products.json"):
        """
        Initialize the DropshipAgent with the given file path to save products.
        """
        self.save_path = save_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.writer = AIWriter()

    def fetch_aliexpress_products(self, keyword: str = "wireless earphones", limit: int = 5) -> List[Dict]:
        """
        Fetch product listings from AliExpress using a search keyword.

        :param keyword: Product search term
        :param limit: Max number of products to return
        :return: List of product dictionaries
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        search_url = f"https://www.aliexpress.com/wholesale?SearchText={keyword.replace(' ', '+')}"

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            log_task("dropship_scrape", "error", f"AliExpress fetch failed: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        products = self._parse_aliexpress(soup, limit)
        return products

    def fetch_ebay_trending(self, limit: int = 5) -> List[Dict]:
        """
        Scrapes trending items from eBay.

        :param limit: Max items to return
        :return: List of trending product dictionaries
        """
        url = "https://www.ebay.com/trending"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            log_task("dropship_scrape", "error", f"eBay fetch failed: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        return self._parse_ebay(soup, limit)

    def _parse_aliexpress(self, soup: BeautifulSoup, limit: int) -> List[Dict]:
        """
        Extracts products from AliExpress page soup.

        :param soup: Parsed HTML content
        :param limit: Max number of items
        :return: List of products
        """
        products = []

        for script in soup.find_all("script"):
            if "window.runParams" in str(script):
                try:
                    match = re.search(r'window\.runParams\s*=\s*({.*?});', str(script), re.DOTALL)
                    if match:
                        data = json.loads(match.group(1))
                        items = data.get("mods", {}).get("itemList", {}).get("content", [])[:limit]

                        for item in items:
                            title = item.get("title", "No title")
                            product = {
                                "title": title,
                                "price": item.get("price", {}).get("formattedPrice", "N/A"),
                                "image": item.get("image", "").split("_")[0] + ".jpg",
                                "url": f"https:{item.get('productUrl', '')}",
                                "source": "aliexpress"
                            }
                            product["ai_description"] = self._generate_description(title)
                            products.append(product)
                except Exception as e:
                    log_task("dropship_scrape", "error", f"AliExpress parse failed: {e}")
                break

        self._save_products(products)
        return products

    def _parse_ebay(self, soup: BeautifulSoup, limit: int) -> List[Dict]:
        """
        Parses trending eBay items from page.

        :param soup: Parsed HTML content
        :param limit: Max number of items
        :return: List of product dictionaries
        """
        results = []
        items = soup.select(".b-module .b-trending-item")

        for item in items[:limit]:
            title_tag = item.select_one("h3")
            img_tag = item.select_one("img")

            title = title_tag.text.strip() if title_tag else "Untitled"
            image = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""

            result = {
                "title": title,
                "image": image,
                "source": "ebay",
                "ai_description": self._generate_description(title)
            }
            results.append(result)

        self._save_products(results)
        return results

    def _generate_description(self, title: str) -> str:
        """
        Generates an AI-enhanced product description.

        :param title: Product title
        :return: Rewritten product description
        """
        try:
            return self.writer.rewrite_product(title)
        except Exception as e:
            log_task("ai_writer", "fail", f"Failed to rewrite: {e}")
            return title

    def _save_products(self, products: List[Dict]):
        """
        Saves fetched product data to disk.

        :param products: List of product dicts
        """
        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(products, f, indent=2)
            log_task("dropship_scrape", "save", f"{len(products)} items saved.")
        except Exception as e:
            log_task("dropship_scrape", "error", f"Failed to save products: {e}")
