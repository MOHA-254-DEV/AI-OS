import time
import logging
from .store import EventStore
from .serializer import deserialize_event
# from core.event_bus import event_bus  # Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ReplayEngine:
    def __init__(self, speed=1.0):
        """
        Initialize the replay engine.

        Args:
            speed (float): Replay speed multiplier (e.g., 1.0 = real-time, 10.0 = 10x faster).
        """
        self.store = EventStore()
        self.speed = speed

    def replay(self, agent_id=None, max_events=None, emit=False):
        """
        Replays historical events for a given agent or all agents.

        Args:
            agent_id (str, optional): Replay events for a specific agent only.
            max_events (int, optional): Maximum number of events to replay.
            emit (bool): Whether to emit the event back to the event bus.
        """
        events = self.store.get_all() if agent_id is None else self.store.get_events_by_agent(agent_id)
        events = [deserialize_event(e) for e in events]
        events.sort(key=lambda x: x["timestamp"])

        if not events:
            logger.warning("⚠️ No events to replay.")
            return

        for i, event in enumerate(events):
            if max_events and i >= max_events:
                break

            delay = 0
            if i > 0:
                delay = (event["timestamp"] - events[i - 1]["timestamp"]) / self.speed
            time.sleep(delay)

            logger.info(f"[{event['agent_id']}] -> {event['event_type']} @ {event['timestamp']} :: {event['content']}")

            if emit:
                # event_bus.publish(event["event_type"], event["content"])
                pass
