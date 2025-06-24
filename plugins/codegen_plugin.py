from agents.dev_agent import DevAgent
from utils.logger import log_task

async def list_templates(args):
    agent = DevAgent()
    templates = agent.list_templates()
    log_task("list_templates", "success", f"{len(templates)} templates")
    return {"templates": templates}

async def scaffold_project(args):
    if len(args) < 2:
        return {"error": "Usage: scaffold_project <template> <project_name>"}
    template, name = args[0], args[1]
    agent = DevAgent()
    result = agent.generate_project(template, name)
    log_task("scaffold_project", "success" if "error" not in result else "failed", str(result))
    return result

def register():
    return {
        "list_templates": list_templates,
        "scaffold_project": scaffold_project
    }
