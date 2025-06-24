from agents.trading_agent import TradingAgent
from utils.logger import log_task

async def check_crypto(args):
    coin = args[0] if args else "bitcoin"
    agent = TradingAgent()
    price = agent.fetch_crypto_price(coin)
    log_task("check_crypto", "success" if price else "failed", f"{coin} = {price}")
    return {"coin": coin, "price": price}

async def analyze_forex(args):
    from_symbol = args[0] if len(args) > 0 else "USD"
    to_symbol = args[1] if len(args) > 1 else "KES"
    agent = TradingAgent()
    prices = agent.fetch_forex_data(from_symbol, to_symbol)
    result = agent.analyze_signals(prices)
    log_task("analyze_forex", "success" if isinstance(result, dict) else "failed", f"{from_symbol}/{to_symbol}")
    return result

def register():
    return {
        "check_crypto": check_crypto,
        "analyze_forex": analyze_forex
    }
