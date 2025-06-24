from agents.marketing_agent import MarketingAgent
from utils.logger import log_task

async def generate_ad_copy(args):
    if len(args) < 2:
        return {"error": "Usage: generate_ad_copy <niche> <product> [benefit]"}
    niche, product = args[0], args[1]
    benefit = args[2] if len(args) > 2 else "amazing performance"
    agent = MarketingAgent()
    result = agent.generate_ad_copy(niche, product, benefit)
    log_task("generate_ad_copy", "success", result)
    return {"ad_copy": result}

async def seo_optimize(args):
    if not args:
        return {"error": "Usage: seo_optimize <topic>"}
    topic = " ".join(args)
    agent = MarketingAgent()
    result = agent.seo_optimize_title(topic)
    log_task("seo_optimize", "success", result)
    return {"seo_title": result}

async def crawl_keywords(args):
    if not args:
        return {"error": "Usage: crawl_keywords <url>"}
    url = args[0]
    agent = MarketingAgent()
    result = agent.crawl_keywords(url)
    log_task("crawl_keywords", "success", str(result))
    return {"keywords": result}

async def summarize_page(args):
    if not args:
        return {"error": "Usage: summarize_page <url>"}
    url = args[0]
    agent = MarketingAgent()
    result = agent.summarize_page(url)
    log_task("summarize_page", "success", str(result))
    return {"summary": result}

def register():
    return {
        "generate_ad_copy": generate_ad_copy,
        "seo_optimize": seo_optimize,
        "crawl_keywords": crawl_keywords,
        "summarize_page": summarize_page
    }
