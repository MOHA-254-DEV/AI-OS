# /core/event_bus/subscribers/retry_subscriber.py
import logging
from ..event_bus import event_bus
from ..event_types import EventType

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def retry_failed_task(payload):
    task_id = payload.get("task_id")
    agent_id = payload.get("agent_id", "unknown")

    if not task_id:
        logger.warning("[RetrySubscriber] Received TASK_RETRY without a task_id.")
        return

    logger.info(f"[RetrySubscriber] Retrying task '{task_id}' for agent '{agent_id}'.")

    # TODO: Replace with actual retry mechanism
    # retry_queue.put(task_id) or orchestrator.reschedule(task_id)

event_bus.subscribe(EventType.TASK_RETRY, retry_failed_task)
