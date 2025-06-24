import requests
import os
import statistics
from secure.crypto_util import decrypt_data
from utils.logger import logger

# Constants
RSI_PERIOD = 14  # Default RSI window
SMA_PERIOD = 14  # Default SMA window


class TradingAgent:
    def __init__(self):
        self.api_key = self._load_api_key()

    def _load_api_key(self):
        """
        Securely load and decrypt the Alpha Vantage API key.
        """
        path = "secure/secrets/alphavantage.token"
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    key = decrypt_data(f.read())
                    logger.info("Alpha Vantage API key loaded.")
                    return key
            except Exception as e:
                logger.error(f"Error decrypting API key: {e}")
        else:
            logger.error("Alpha Vantage API key file not found.")
        return None

    def fetch_forex_data(self, from_symbol="USD", to_symbol="KES"):
        """
        Fetch daily closing Forex prices for the specified currency pair.
        """
        if not self.api_key:
            logger.error("API key is missing.")
            return []

        url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_symbol}&to_symbol={to_symbol}&apikey={self.api_key}&outputsize=compact"
        logger.info(f"Fetching Forex rates for {from_symbol}/{to_symbol}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json().get("Time Series FX (Daily)", {})

            if not data:
                logger.warning(f"No data returned for {from_symbol}/{to_symbol}.")
                return []

            prices = [float(entry["4. close"]) for entry in list(data.values())[:RSI_PERIOD]]
            return prices
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Forex data: {e}")
            return []

    def fetch_crypto_price(self, coin_id="bitcoin", vs="usd"):
        """
        Fetch the current price of a cryptocurrency from CoinGecko.
        """
        logger.info(f"Fetching price for {coin_id} in {vs}")
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            price = data.get(coin_id, {}).get(vs)
            if price is None:
                logger.error(f"Price not available for {coin_id}/{vs}")
                return {"error": "Price unavailable"}
            return {"coin": coin_id, "currency": vs, "price": price}
        except requests.RequestException as e:
            logger.error(f"Error fetching crypto price: {e}")
            return {"error": str(e)}

    def calculate_rsi(self, prices):
        """
        Calculate the Relative Strength Index (RSI) for a list of closing prices.
        :param prices: List of float closing prices.
        :return: RSI value or None if not enough data.
        """
        if len(prices) < RSI_PERIOD:
            logger.warning("Not enough data to calculate RSI.")
            return None

        logger.info("Calculating RSI.")
        gains, losses = [], []
        for i in range(1, RSI_PERIOD):
            delta = prices[i - 1] - prices[i]
            if delta > 0:
                gains.append(delta)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-delta)

        avg_gain = sum(gains) / RSI_PERIOD
        avg_loss = sum(losses) / RSI_PERIOD

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        logger.info(f"RSI calculated: {rsi:.2f}")
        return round(rsi, 2)

    def calculate_sma(self, prices):
        """
        Calculate the Simple Moving Average (SMA) for a list of prices.
        :param prices: List of float prices.
        :return: SMA value or None if insufficient data.
        """
        if len(prices) < SMA_PERIOD:
            logger.warning("Not enough data to calculate SMA.")
            return None

        sma = statistics.mean(prices[:SMA_PERIOD])
        logger.info(f"SMA calculated: {sma:.2f}")
        return round(sma, 2)

    def analyze_forex_pair(self, base="USD", quote="KES"):
        """
        High-level analysis on a Forex pair (RSI + SMA).
        """
        logger.info(f"Starting analysis for {base}/{quote}")
        prices = self.fetch_forex_data(from_symbol=base, to_symbol=quote)
        if not prices:
            return {"error": "No price data available"}

        rsi = self.calculate_rsi(prices)
        sma = self.calculate_sma(prices)

        return {
            "pair": f"{base}/{quote}",
            "latest_price": prices[0] if prices else None,
            "rsi": rsi,
            "sma": sma
        }
