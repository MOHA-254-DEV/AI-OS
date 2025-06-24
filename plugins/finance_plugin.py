from agents.finance_agent import FinanceAgent
from utils.logger import log_task

agent = FinanceAgent()

async def market_summary(args):
    result = agent.market_summary()
    log_task("market_summary", "complete", str(result))
    return result

async def simulate_trade(args):
    if len(args) < 4:
        return {"error": "Usage: simulate_trade <portfolio_name> <asset> <buy/sell> <qty>"}
    name, asset, action, qty = args[0], args[1], args[2], int(args[3])
    result = agent.simulate_trade(name, asset, action, qty)
    log_task("simulate_trade", "complete", str(result))
    return result

async def build_portfolio(args):
    if not args:
        return {"error": "Usage: build_portfolio <portfolio_name>"}
    result = agent.build_portfolio(args[0])
    log_task("build_portfolio", "complete", str(result))
    return result

async def track_asset(args):
    if not args:
        return {"error": "Usage: track_asset <asset_name>"}
    result = agent.track_asset(args[0])
    log_task("track_asset", "complete", str(result))
    return result

def register():
    return {
        "market_summary": market_summary,
        "simulate_trade": simulate_trade,
        "build_portfolio": build_portfolio,
        "track_asset": track_asset
    }
