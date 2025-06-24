from typing import Callable, Dict, List, Any
from threading import Lock
import logging

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Any], None]]] = {}
        self.lock = Lock()

    def subscribe(self, event_type: str, handler: Callable[[Any], None]):
        """
        Register a handler for a specific event type.

        Args:
            event_type (str): The event identifier.
            handler (Callable): A function to handle the event.
        """
        with self.lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            if handler not in self.subscribers[event_type]:  # Prevent duplicate registration
                self.subscribers[event_type].append(handler)
                logger.info(f"Handler subscribed to event: {event_type}")
            else:
                logger.debug(f"Handler already subscribed to event: {event_type}")

    def publish(self, event_type: str, payload: Any):
        """
        Emit an event and notify all registered handlers.

        Args:
            event_type (str): The type of event.
            payload (Any): The data to pass to each handler.
        """
        with self.lock:
            handlers = list(self.subscribers.get(event_type, []))  # copy to avoid mutation during iteration

        logger.info(f"Publishing event: {event_type} to {len(handlers)} handlers")

        for handler in handlers:
            try:
                handler(payload)
            except Exception as e:
                logger.exception(f"[EventBus] Error in handler for event '{event_type}': {e}")

# Global singleton
event_bus = EventBus()
