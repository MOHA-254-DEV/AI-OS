# File: /core/realtime/agent_hooks/dispatcher.py

from ..pubsub.subscriber import subscribe_to_topic
from ..pubsub.topics import Topics
from core.logging.plugin_logger import PluginLogger

logger = PluginLogger()

def handle_agent_status(data):
    try:
        logger.log("AgentDispatcher", input_code="AGENT_STATUS", output=str(data), success=True)
        print(f"[Dispatcher] Agent status updated: {data}")
        # Future: update internal registry or health dashboard
    except Exception as e:
        logger.log("AgentDispatcher", input_code="AGENT_STATUS", output="", success=False, error=str(e))

def handle_task_update(data):
    try:
        logger.log("AgentDispatcher", input_code="TASK_UPDATE", output=str(data), success=True)
        print(f"[Dispatcher] Task update received: {data}")
        # Future: trigger agent re-planning, audit task
    except Exception as e:
        logger.log("AgentDispatcher", input_code="TASK_UPDATE", output="", success=False, error=str(e))

def init_hooks():
    """
    Register real-time hook listeners for agent events.
    """
    try:
        subscribe_to_topic(Topics.AGENT_STATUS, handle_agent_status)
        subscribe_to_topic(Topics.TASK_UPDATE, handle_task_update)
        print("[Dispatcher] Hooks initialized for agent.")
    except Exception as e:
        logger.log("AgentDispatcher", input_code="init_hooks", output="", success=False, error=str(e))
