# /core/event_bus/subscribers/memory_subscriber.py
import logging
from datetime import datetime
from ..event_bus import event_bus
from ..event_types import EventType

# Basic in-memory storage (replace with proper memory module later)
memory_store = []

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def store_event_in_memory(payload):
    timestamp = datetime.utcnow().isoformat()
    memory_record = {
        "timestamp": timestamp,
        "event": payload
    }

    memory_store.append(memory_record)

    logger.info(f"[MemorySubscriber] Stored event at {timestamp}: {payload}")

# Subscribe to relevant memory-influencing events
event_bus.subscribe(EventType.TASK_COMPLETED, store_event_in_memory)
event_bus.subscribe(EventType.TASK_FEEDBACK, store_event_in_memory)
