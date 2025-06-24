from agents.neteng_agent import NetworkEngineeringAgent
from utils.logger import log_task

agent = NetworkEngineeringAgent()

async def ping_server(args):
    if not args:
        return {"error": "Usage: ping_server <hostname>"}
    result = agent.ping_server(args[0])
    log_task("ping_server", "complete", str(result))
    return result

async def check_usage(args):
    result = agent.check_usage()
    log_task("check_usage", "complete", str(result))
    return result

async def deploy_script(args):
    if len(args) < 3:
        return {"error": "Usage: deploy_script <name> <lang> <code_string>"}
    name, lang, *code = args
    code_str = " ".join(code)
    result = agent.deploy_script(name, code_str, lang)
    log_task("deploy_script", "success", str(result))
    return result

async def run_script(args):
    if len(args) < 2:
        return {"error": "Usage: run_script <name> <lang>"}
    result = agent.run_script(args[0], args[1])
    log_task("run_script", "complete", str(result))
    return result

async def monitor_logs(args):
    if not args:
        return {"error": "Usage: monitor_logs <log_file_path>"}
    result = agent.monitor_logs(args[0])
    log_task("monitor_logs", "complete", str(result))
    return result

def register():
    return {
        "ping_server": ping_server,
        "check_usage": check_usage,
        "deploy_script": deploy_script,
        "run_script": run_script,
        "monitor_logs": monitor_logs
    }
