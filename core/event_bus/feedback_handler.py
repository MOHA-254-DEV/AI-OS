import datetime
import logging
from .event_bus import event_bus
from .event_types import EventType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FeedbackHandler:
    def __init__(self):
        event_bus.subscribe(EventType.TASK_COMPLETED, self.log_success)
        event_bus.subscribe(EventType.TASK_FAILED, self.log_failure)
        event_bus.subscribe(EventType.TASK_FEEDBACK, self.log_feedback)

    def log_success(self, payload):
        task_id = payload.get("task_id", "unknown")
        msg = payload.get("msg", "")
        logger.info(f"[{datetime.datetime.now()}] ✅ Task completed: {task_id} | {msg}")

    def log_failure(self, payload):
        task_id = payload.get("task_id", "unknown")
        reason = payload.get("reason", "Unknown")
        logger.error(f"[{datetime.datetime.now()}] ❌ Task failed: {task_id} | Reason: {reason}")

        # Trigger retry unless opted out
        if not payload.get("no_retry", False):
            event_bus.publish(EventType.TASK_RETRY, payload)

    def log_feedback(self, payload):
        task_id = payload.get("task_id", "unknown")
        feedback = payload.get("feedback", "")
        logger.debug(f"[{datetime.datetime.now()}] 💬 Feedback: {task_id} | {feedback}")

feedback_handler = FeedbackHandler()
