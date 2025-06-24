from ai.planner import Planner
from utils.logger import log_task

planner = Planner()

async def interpret_prompt(args):
    if not args:
        return {"error": "Usage: interpret_prompt <natural_prompt>"}
    prompt = " ".join(args)
    result = planner.plan_from_prompt(prompt)
    log_task("interpret_prompt", "complete", str(result))
    return result

async def route_prompt(args):
    if not args:
        return {"error": "Usage: route_prompt <goal_instruction>"}
    goal = " ".join(args)
    result = planner.generate_task_chain(goal)
    log_task("route_prompt", "complete", str(result))
    return result

def register():
    return {
        "interpret_prompt": interpret_prompt,
        "route_prompt": route_prompt
    }
