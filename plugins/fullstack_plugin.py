from agents.fullstack_agent import FullStackAgent
from utils.logger import log_task

agent = FullStackAgent()

async def generate_app(args):
    if len(args) < 1:
        return {"error": "Usage: generate_app <app_name> [stack]"}
    name = args[0]
    stack = args[1] if len(args) > 1 else "react-flask"
    result = agent.generate_app(name, stack)
    log_task("generate_app", "success", str(result))
    return result

async def build_crud(args):
    if len(args) < 2:
        return {"error": "Usage: build_crud <app_name> <model_fields>"}
    name = args[0]
    model = " ".join(args[1:])
    result = agent.build_crud(name, model)
    log_task("build_crud", "success", str(result))
    return result

async def deploy_stack(args):
    if not args:
        return {"error": "Usage: deploy_stack <app_name>"}
    name = args[0]
    result = agent.deploy_stack(name)
    log_task("deploy_stack", "success", str(result))
    return result

def register():
    return {
        "generate_app": generate_app,
        "build_crud": build_crud,
        "deploy_stack": deploy_stack
    }
