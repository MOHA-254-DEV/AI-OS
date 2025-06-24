"""
agent_messenger.py

Handles agent-to-agent message routing within the AI operating system.
Uses an event-driven architecture through the shared event bus.
"""

from .agent_protocol import AgentMessage
from core.event_bus.event_bus import event_bus
from core.event_bus.event_types import EventType
import core.agent_messaging.handlers.command_handler as command_handler
import core.agent_messaging.handlers.status_handler as status_handler
import core.agent_messaging.handlers.error_handler as error_handler
import logging
from typing import Callable, Dict

# Setup logger
logger = logging.getLogger("AgentMessenger")
logger.setLevel(logging.INFO)

class AgentMessenger:
    """
    Responsible for handling incoming/outgoing agent messages via event_bus.
    Routes based on command type.
    """

    def __init__(self):
        # Subscribe to message events
        event_bus.subscribe(EventType.AGENT_MESSAGE, self.route_message)
        logger.info("[AgentMessenger] Subscribed to AGENT_MESSAGE events.")

        # Routing table
        self.command_routes: Dict[str, Callable[[AgentMessage], None]] = {
            "status": status_handler.handle,
            "cmd": command_handler.handle
        }

    def send(self, message: AgentMessage):
        """
        Send an agent message via the event bus.
        """
        if not isinstance(message, AgentMessage):
            raise TypeError("Message must be an instance of AgentMessage")

        try:
            logger.info(f"[AgentMessenger] Dispatching {message.command} from {message.sender} to {message.receiver}")
            event_bus.publish(EventType.AGENT_MESSAGE, message.to_dict())
        except Exception as e:
            logger.error(f"[AgentMessenger] Failed to send message: {e}")
            error_handler.handle(message.to_dict(), str(e))

    def route_message(self, message_dict: dict):
        """
        Route incoming message dictionary to the appropriate handler.
        """
        if not isinstance(message_dict, dict):
            logger.error("[AgentMessenger] Message must be a dictionary.")
            return

        try:
            message = AgentMessage.from_dict(message_dict)
            command_key = self._extract_command_key(message.command)

            handler = self.command_routes.get(command_key)

            if handler:
                logger.info(f"[AgentMessenger] Routing '{message.command}' → {handler.__module__}.{handler.__name__}")
                handler(message)
            else:
                logger.warning(f"[AgentMessenger] No handler found for command '{message.command}'")
                error_handler.handle(message_dict, f"No handler for command '{message.command}'")

        except Exception as e:
            logger.exception("[AgentMessenger] Error during message routing")
            error_handler.handle(message_dict, str(e))

    def register_handler(self, command_prefix: str, handler_func: Callable[[AgentMessage], None]):
        """
        Dynamically register a new command handler.
        """
        if not callable(handler_func):
            raise ValueError("Handler must be a callable function.")
        self.command_routes[command_prefix.strip().lower()] = handler_func
        logger.info(f"[AgentMessenger] Registered new handler for '{command_prefix}'")

    def _extract_command_key(self, command: str) -> str:
        """
        Extract command prefix from full command string.
        Example: 'cmd:reset' → 'cmd'
        """
        return command.split(":")[0].strip().lower() if ":" in command else command.strip().lower()
