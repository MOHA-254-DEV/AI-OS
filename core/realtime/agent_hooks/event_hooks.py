# File: /core/realtime/agent_hooks/event_hooks.py

from ..pubsub import publish_event
from ..pubsub.topics import Topics
from core.logging.plugin_logger import PluginLogger

logger = PluginLogger()

def on_agent_status_change(agent_id: str, status: str) -> None:
    event = {'id': agent_id, 'status': status}
    try:
        publish_event(Topics.AGENT_STATUS, event)
        logger.log("EventHook", input_code="AGENT_STATUS_CHANGE", output=str(event), success=True)
    except Exception as e:
        logger.log("EventHook", input_code="AGENT_STATUS_CHANGE", output="", success=False, error=str(e))

def on_task_update(task_id: str, result: str) -> None:
    event = {'task': task_id, 'result': result}
    try:
        publish_event(Topics.TASK_UPDATE, event)
        logger.log("EventHook", input_code="TASK_UPDATE", output=str(event), success=True)
    except Exception as e:
        logger.log("EventHook", input_code="TASK_UPDATE", output="", success=False, error=str(e))

def on_error_event(error: str) -> None:
    event = {'error': error}
    try:
        publish_event(Topics.ERROR_EVENT, event)
        logger.log("EventHook", input_code="ERROR_EVENT", output=str(event), success=True)
    except Exception as e:
        logger.log("EventHook", input_code="ERROR_EVENT", output="", success=False, error=str(e))
