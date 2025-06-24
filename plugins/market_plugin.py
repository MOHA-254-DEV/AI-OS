from agents.market_agent import MarketAgent
from utils.logger import log_task

agent = MarketAgent()

async def crypto_price(args):
    symbol = args[0] if args else "bitcoin"
    result = agent.fetch_crypto_price(symbol)
    log_task("crypto_price", "fetch", str(result))
    return result

async def stock_price(args):
    symbol = args[0] if args else "AAPL"
    result = agent.fetch_stock_price(symbol)
    log_task("stock_price", "fetch", str(result))
    return result

async def forex_rate(args):
    if len(args) < 2:
        return {"error": "Usage: forex_rate <BASE> <QUOTE>"}
    base, quote = args[0], args[1]
    result = agent.fetch_forex_price(base, quote)
    log_task("forex_rate", "fetch", str(result))
    return result

async def crypto_history(args):
    symbol = args[0] if len(args) > 0 else "bitcoin"
    days = int(args[1]) if len(args) > 1 else 7
    result = agent.historical_crypto(symbol, days)
    log_task("crypto_history", "fetch", str(result))
    return result

async def market_cache(args):
    return agent.get_cache()

def register():
    return {
        "crypto_price": crypto_price,
        "stock_price": stock_price,
        "forex_rate": forex_rate,
        "crypto_history": crypto_history,
        "market_cache": market_cache
    }
