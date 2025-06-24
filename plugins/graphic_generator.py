from agents.graphic_agent import GraphicAgent
from utils.logger import log_task

async def generate_banner(args):
    prompt = " ".join(args) if args else "futuristic AI logo"
    agent = GraphicAgent()
    output = agent.generate_image(prompt)
    log_task("generate_banner", "success" if output else "failed", prompt)
    return output

def register():
    return {
        "generate_banner": generate_banner
    }
