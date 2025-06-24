from agents.dropshipping_agent import DropshippingAgent
from utils.logger import log_task
from agents.dropshipping_agent import DropshippingAgent
from utils.logger import log_task


async def list_products(args):
    agent = DropshippingAgent()
    products = agent.get_products()
    log_task("list_products", "success" if products else "failed", f"{len(products)} products listed")
    return products

async def add_product(args):
    title = args[0] if args else "Default Product"
    body = " ".join(args[1:]) if len(args) > 1 else "<p>Auto-listed by AI</p>"
    agent = DropshippingAgent()
    result = agent.create_product(title, body, "19.99")
    log_task("add_product", "success" if result else "failed", title)
    return result

def register():
    return {
        "list_products": list_products,
        "add_product": add_product
    }
    agent = DropshippingAgent()

async def fetch_products(args):
    result = agent.fetch_products()
    log_task("fetch_products", "success", str(result))
    return {"products": result}

async def update_price(args):
    margin = float(args[0]) if args else 0.25
    result = agent.update_prices(margin)
    log_task("update_price", "success", f"Margin: {margin}")
    return {"updated_prices": result}

async def create_storefront(args):
    products = agent.generate_storefront_data()
    log_task("create_storefront", "success", f"{len(products)} products loaded")
    return {"status": "ready", "frontend_file": "frontend/Storefront.jsx"}

def register():
    return {
        "fetch_products": fetch_products,
        "update_price": update_price,
        "create_storefront": create_storefront
    }
