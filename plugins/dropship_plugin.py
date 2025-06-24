from agents.dropship_agent import DropshipAgent

agent = DropshipAgent()

async def aliexpress_products(args):
    keyword = " ".join(args) if args else "wireless charger"
    results = agent.fetch_aliexpress_products(keyword)
    return results

async def ebay_trending(args):
    return agent.fetch_ebay_trending()

async def list_dropship_products(args):
    return agent.list_saved()

def register():
    return {
        "aliexpress_products": aliexpress_products,
        "ebay_trending": ebay_trending,
        "list_dropship_products": list_dropship_products
    }
