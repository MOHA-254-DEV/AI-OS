import time
import logging
from .store import EventStore
from .serializer import serialize_event

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EventLogger:
    def __init__(self):
        self.store = EventStore()

    def log(self, agent_id, event_type, content, timestamp=None):
        """
        Logs an event for an agent.

        Args:
            agent_id (str): ID of the agent.
            event_type (str): Type of the event.
            content (str or dict): Event payload/content.
            timestamp (float, optional): Unix timestamp. Defaults to now.
        """
        try:
            timestamp = timestamp or time.time()
            event = {
                "timestamp": timestamp,
                "agent_id": agent_id,
                "event_type": event_type,
                "content": content
            }
            serialized = serialize_event(event)
            self.store.save_event(serialized)
        except Exception as e:
            logger.error(f"[EventLogger] Failed to log event: {e}")

    def get_agent_events(self, agent_id):
        return self.store.get_events_by_agent(agent_id)

    def get_all_events(self):
        return self.store.get_all()

    def get_events_by_type(self, event_type):
        return [e for e in self.get_all_events() if e.get("event_type") == event_type]
