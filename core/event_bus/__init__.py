"""
Initializes the Event Bus system and registers core event subscribers and handlers.
"""

from .event_bus import event_bus
from .event_types import EventType
from .feedback_handler import feedback_handler

# Register subscribers
import core.event_bus.subscribers.log_subscriber
import core.event_bus.subscribers.memory_subscriber
import core.event_bus.subscribers.retry_subscriber
