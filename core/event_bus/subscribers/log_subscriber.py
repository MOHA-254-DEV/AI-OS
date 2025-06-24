# /core/event_bus/subscribers/log_subscriber.py
import logging
from datetime import datetime
from ..event_bus import event_bus
from ..event_types import EventType

# Configure logging (optional: move to global config)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def log_task_event(payload):
    timestamp = datetime.utcnow().isoformat()
    logger.info(f"[LogSubscriber] [{timestamp}] Event received: {payload}")

# Subscribe to task-related and message events
event_bus.subscribe(EventType.TASK_STARTED, log_task_event)
event_bus.subscribe(EventType.AGENT_MESSAGE, log_task_event)
