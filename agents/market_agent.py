import requests
import json
import os
from datetime import datetime, timedelta
from utils.logger import log_task


class MarketAgent:
    def __init__(self, cache_file="data/market/cache.json", cache_expiry_minutes=10):
        self.cache_file = cache_file
        self.cache_expiry_minutes = cache_expiry_minutes
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    def _now(self):
        return datetime.utcnow().isoformat()

    def _save_cache(self, key, data):
        try:
            cache = self._load_cache()
            cache[key] = {
                "data": data,
                "time": self._now()
            }
            with open(self.cache_file, "w") as f:
                json.dump(cache, f, indent=4)
            log_task("market_agent", "cache_saved", f"{key} at {self._now()}")
        except Exception as e:
            log_task("market_agent", "cache_error", f"{key} save error: {str(e)}")

    def _load_cache(self):
        if not os.path.exists(self.cache_file):
            return {}
        try:
            with open(self.cache_file, "r") as f:
                return json.load(f)
        except Exception as e:
            log_task("market_agent", "cache_error", f"Read error: {str(e)}")
            return {}

    def _is_cache_expired(self, timestamp):
        try:
            cache_time = datetime.fromisoformat(timestamp)
            return (datetime.utcnow() - cache_time) > timedelta(minutes=self.cache_expiry_minutes)
        except Exception:
            return True

    def _get_from_cache(self, key):
        cache = self._load_cache()
        entry = cache.get(key)
        if entry and not self._is_cache_expired(entry.get("time", "")):
            log_task("market_agent", "cache_hit", key)
            return entry["data"]
        return None

    def fetch_crypto_price(self, symbol="bitcoin"):
        key = f"crypto_{symbol}"
        cached = self._get_from_cache(key)
        if cached:
            return cached

        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
            res = requests.get(url)
            res.raise_for_status()
            usd = res.json().get(symbol, {}).get("usd")
            if usd is None:
                raise ValueError("Price missing in API response")

            result = {"symbol": symbol, "price_usd": round(usd, 4), "timestamp": self._now()}
            self._save_cache(key, result)
            return result
        except Exception as e:
            return {"error": f"Failed to fetch crypto price: {str(e)}"}

    def fetch_stock_price(self, symbol="AAPL"):
        key = f"stock_{symbol}"
        cached = self._get_from_cache(key)
        if cached:
            return cached

        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            data = res.json()
            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]

            result = {"symbol": symbol.upper(), "price": round(price, 4), "timestamp": self._now()}
            self._save_cache(key, result)
            return result
        except Exception as e:
            return {"error": f"Failed to fetch stock price for {symbol}: {str(e)}"}

    def fetch_forex_price(self, base="USD", quote="EUR"):
        key = f"forex_{base}_{quote}"
        cached = self._get_from_cache(key)
        if cached:
            return cached

        try:
            url = f"https://api.exchangerate.host/latest?base={base}&symbols={quote}"
            res = requests.get(url)
            res.raise_for_status()
            rate = res.json()["rates"].get(quote)

            if rate is None:
                raise ValueError("Rate not found")

            result = {"pair": f"{base}/{quote}", "rate": round(rate, 6), "timestamp": self._now()}
            self._save_cache(key, result)
            return result
        except Exception as e:
            return {"error": f"Failed to fetch forex rate for {base}/{quote}: {str(e)}"}

    def historical_crypto(self, symbol="bitcoin", days=7):
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days={days}"
            res = requests.get(url)
            res.raise_for_status()
            prices = res.json().get("prices", [])
            history = [
                {"date": datetime.utcfromtimestamp(ts / 1000).isoformat(), "price": round(price, 4)}
                for ts, price in prices
            ]
            return {"symbol": symbol, "days": days, "history": history}
        except Exception as e:
            return {"error": f"Failed to fetch historical data for {symbol}: {str(e)}"}

    def get_cache(self):
        try:
            return self._load_cache()
        except Exception as e:
            return {"error": f"Could not load cache: {str(e)}"}


# Example usage
if __name__ == "__main__":
    agent = MarketAgent()

    print("🔹 Crypto:", agent.fetch_crypto_price("bitcoin"))
    print("🔹 Stock:", agent.fetch_stock_price("AAPL"))
    print("🔹 Forex:", agent.fetch_forex_price("USD", "EUR"))
    print("🔹 History:", agent.historical_crypto("bitcoin", days=3))
    print("📦 Full Cache:", json.dumps(agent.get_cache(), indent=2))
