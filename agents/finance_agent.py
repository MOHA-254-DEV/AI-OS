import os
import json
import random
import requests
from datetime import datetime
from typing import Dict, Optional, List, Union
from utils.logger import logger
from secure.crypto_util import decrypt_data


class FinanceAgent:
    def __init__(self, portfolio_dir: str = "data/portfolios", assets: Optional[List[str]] = None):
        self.portfolio_dir = portfolio_dir
        os.makedirs(self.portfolio_dir, exist_ok=True)

        self.assets = assets if assets else ["AAPL", "TSLA", "BTC", "ETH", "GOOG", "USD", "EUR", "JPY"]
        self.api_key = self.load_api_key()

    def load_api_key(self) -> Optional[str]:
        """
        Loads API key from secure storage.
        """
        key_path = "secure/secrets/api_key.txt"
        if os.path.exists(key_path):
            try:
                with open(key_path, "r") as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"[FinanceAgent] Failed to read API key: {e}")
        else:
            logger.warning("[FinanceAgent] API key file not found.")
        return None

    def _portfolio_path(self, name: str) -> str:
        return os.path.join(self.portfolio_dir, f"{name}.json")

    def _load_portfolio(self, name: str) -> Dict:
        path = self._portfolio_path(name)
        if not os.path.exists(path):
            logger.info(f"[FinanceAgent] Creating new portfolio '{name}'.")
            return {"cash": 10000.0, "assets": {}, "history": []}
        with open(path, "r") as f:
            return json.load(f)

    def _save_portfolio(self, name: str, data: Dict):
        with open(self._portfolio_path(name), "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"[FinanceAgent] Portfolio '{name}' saved.")

    def fetch_real_time_price(self, asset: str) -> Optional[float]:
        """
        Fetch real-time price from Coingecko or AlphaVantage.
        """
        try:
            asset = asset.upper()
            if asset in ["BTC", "ETH"]:
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={asset.lower()}&vs_currencies=usd"
                res = requests.get(url, timeout=10)
                data = res.json()
                return float(data[asset.lower()]["usd"])
            elif self.api_key:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={asset}&interval=5min&apikey={self.api_key}"
                res = requests.get(url, timeout=10)
                data = res.json()
                if "Time Series (5min)" in data:
                    latest = list(data["Time Series (5min)"].values())[0]
                    return float(latest.get("4. close", 0))
        except Exception as e:
            logger.warning(f"[FinanceAgent] Price fetch failed for {asset}: {e}")
        return None

    def market_summary(self) -> Dict[str, float]:
        """
        Fetch market summary with fallback on random prices.
        """
        summary = {}
        for asset in self.assets:
            price = self.fetch_real_time_price(asset)
            if price is None:
                price = round(random.uniform(10, 1000), 2)
                logger.debug(f"[FinanceAgent] Used fallback price for {asset}: {price}")
            summary[asset] = price
        return summary

    def simulate_trade(self, portfolio_name: str, asset: str, action: str, quantity: float) -> Dict[str, Union[str, Dict]]:
        """
        Simulate buying or selling an asset.
        """
        asset = asset.upper()
        if quantity <= 0:
            return {"error": "Quantity must be greater than zero."}

        portfolio = self._load_portfolio(portfolio_name)
        market = self.market_summary()
        now = datetime.utcnow().isoformat()

        if asset not in market:
            return {"error": f"Asset '{asset}' not supported."}

        price = market[asset]
        total_cost = round(price * quantity, 2)

        if action == "buy":
            if portfolio["cash"] < total_cost:
                return {"error": "Insufficient cash for this trade."}
            portfolio["cash"] -= total_cost
            portfolio["assets"][asset] = portfolio["assets"].get(asset, 0) + quantity
            portfolio["history"].append({
                "type": "buy", "asset": asset, "qty": quantity, "price": price,
                "cost": total_cost, "timestamp": now
            })

        elif action == "sell":
            if portfolio["assets"].get(asset, 0) < quantity:
                return {"error": f"Not enough {asset} to sell."}
            portfolio["assets"][asset] -= quantity
            portfolio["cash"] += total_cost
            portfolio["history"].append({
                "type": "sell", "asset": asset, "qty": quantity, "price": price,
                "revenue": total_cost, "timestamp": now
            })
        else:
            return {"error": "Invalid action. Use 'buy' or 'sell'."}

        self._save_portfolio(portfolio_name, portfolio)
        logger.info(f"[FinanceAgent] Trade executed: {action} {quantity} {asset} at {price}")
        return {"status": "success", "portfolio": portfolio}

    def build_portfolio(self, name: str) -> Dict:
        """
        Initialize or return an existing portfolio.
        """
        return self._load_portfolio(name)

    def track_asset(self, asset_name: str) -> Dict[str, float]:
        """
        Track current price of a single asset.
        """
        asset = asset_name.upper()
        price = self.fetch_real_time_price(asset)
        return {asset: price or "Unavailable"}

    def update_portfolio_prices(self, portfolio_name: str, margin: float = 0.25) -> Dict:
        """
        Update asset values by applying a margin over current prices.
        """
        portfolio = self._load_portfolio(portfolio_name)
        market = self.market_summary()

        updated_assets = {}
        for asset, qty in portfolio.get("assets", {}).items():
            current_price = market.get(asset, 0)
            marked_price = round(current_price * (1 + margin), 2)
            updated_assets[asset] = marked_price

        portfolio["evaluated_prices"] = updated_assets
        self._save_portfolio(portfolio_name, portfolio)
        return portfolio


# === Example Usage ===
if __name__ == "__main__":
    agent = FinanceAgent()

    name = "smart_portfolio"
    portfolio = agent.build_portfolio(name)
    print("[LOAD]", portfolio)

    result = agent.simulate_trade(name, "AAPL", "buy", 5)
    print("[TRADE]", result)

    asset_price = agent.track_asset("TSLA")
    print("[TRACK]", asset_price)

    updated = agent.update_portfolio_prices(name, margin=0.20)
    print("[UPDATED PORTFOLIO]", updated)
