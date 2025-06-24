import os
import json
import requests
from typing import List, Dict, Optional
from utils.logger import logger
from secure.crypto_util import decrypt_data


class ShopifyDropshippingAgent:
    def __init__(self, token_path="secure/secrets/shopify.token"):
        self.token_path = token_path
        self.base_url = "https://your-shop.myshopify.com/admin/api/2023-04/"
        self.api_key = self._load_api_key()

    def _load_api_key(self) -> Optional[str]:
        """
        Securely load and decrypt the Shopify API token from file.
        """
        if not os.path.exists(self.token_path):
            logger.error(f"[Shopify] Token not found at {self.token_path}")
            return None

        try:
            with open(self.token_path, "rb") as f:
                encrypted = f.read()
                decrypted = decrypt_data(encrypted)
                logger.info("[Shopify] API key loaded successfully.")
                return decrypted
        except Exception as e:
            logger.error(f"[Shopify] Failed to load or decrypt token: {e}")
            return None

    def get_products(self) -> List[Dict]:
        """
        Retrieve a list of products from Shopify.
        """
        if not self.api_key:
            logger.warning("[Shopify] API key not available.")
            return []

        url = f"{self.base_url}products.json"
        headers = {"X-Shopify-Access-Token": self.api_key}
        try:
            logger.info("[Shopify] Fetching products...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            products = response.json().get("products", [])
            logger.info(f"[Shopify] Retrieved {len(products)} products.")
            return products
        except requests.RequestException as e:
            logger.error(f"[Shopify] Product fetch failed: {e}")
            return []

    def create_product(self, title: str, body_html: str, price: float) -> Optional[Dict]:
        """
        Create a new Shopify product.
        """
        if not self.api_key:
            logger.warning("[Shopify] API key not available.")
            return None

        url = f"{self.base_url}products.json"
        headers = {
            "X-Shopify-Access-Token": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "product": {
                "title": title,
                "body_html": body_html,
                "variants": [{"price": str(price)}]
            }
        }

        try:
            logger.info(f"[Shopify] Creating product: {title}")
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            product = response.json()
            logger.info(f"[Shopify] Product '{title}' created successfully.")
            return product
        except requests.RequestException as e:
            logger.error(f"[Shopify] Failed to create product '{title}': {e}")
            return None


class MockDropshippingAgent:
    def __init__(self, data_path="frontend/mock_data.json"):
        self.data_path = data_path
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        if not os.path.exists(data_path):
            self._create_mock_data()

    def _create_mock_data(self):
        """
        Generates default mock product entries.
        """
        mock_products = [
            {"id": 1, "name": "Bluetooth Headphones", "base_price": 25.0, "category": "Electronics"},
            {"id": 2, "name": "Yoga Mat", "base_price": 15.0, "category": "Fitness"},
            {"id": 3, "name": "LED Desk Lamp", "base_price": 18.0, "category": "Home"},
        ]
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(mock_products, f, indent=2)
        logger.info("[MockAgent] Default mock data initialized.")

    def fetch_products(self) -> List[Dict]:
        """
        Retrieve the current mock products list.
        """
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                products = json.load(f)
            logger.info("[MockAgent] Products loaded successfully.")
            return products
        except Exception as e:
            logger.error(f"[MockAgent] Failed to load mock products: {e}")
            return []

    def update_prices(self, margin: float = 0.25) -> List[Dict]:
        """
        Apply a margin to base prices for all products.
        """
        try:
            products = self.fetch_products()
            for p in products:
                p["price"] = round(p["base_price"] * (1 + margin), 2)
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(products, f, indent=2)
            logger.info(f"[MockAgent] Updated prices with {margin*100:.0f}% margin.")
            return products
        except Exception as e:
            logger.error(f"[MockAgent] Failed to update prices: {e}")
            return []

    def generate_storefront_data(self) -> List[Dict]:
        """
        Export formatted mock products for display use.
        """
        return self.fetch_products()


# === Example Usage ===
if __name__ == "__main__":
    # Shopify Test
    shopify_agent = ShopifyDropshippingAgent()
    shopify_products = shopify_agent.get_products()
    print(f"Shopify Products: {shopify_products[:1]}")  # limit output

    # Mock Test
    mock_agent = MockDropshippingAgent()
    print("Original:", mock_agent.fetch_products())
    mock_agent.update_prices(0.3)
    print("Updated Storefront:", mock_agent.generate_storefront_data())
