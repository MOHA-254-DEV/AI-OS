# /core/agent_messaging/handlers/command_handler.py

import logging
from core.agent_messaging.agent_protocol import AgentMessage
from typing import Callable, Dict, Any

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    from logging import StreamHandler
    handler = StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# Optional command registry for extensibility
command_registry: Dict[str, Callable[[AgentMessage], Any]] = {}


def register_command(command_name: str, handler_func: Callable[[AgentMessage], Any]) -> None:
    """
    Register a handler function for a specific command.
    """
    command_registry[command_name] = handler_func
    logger.info(f"[CommandHandler] Registered command: '{command_name}'")


def handle(message: AgentMessage) -> None:
    """
    Entry point for processing a command message.
    Supports dynamic dispatch via `command_registry`.

    Parameters:
    - message (AgentMessage): The message object containing command and payload
    """
    if not isinstance(message, AgentMessage):
        logger.error("[CommandHandler] Invalid message type received.")
        return

    logger.info(
        f"[CommandHandler] Command received by '{message.receiver}': "
        f"{message.command} -> {message.payload}"
    )

    # Route to specific handler if registered
    command_name = message.command.lower()
    handler_func = command_registry.get(command_name)

    if handler_func:
        try:
            result = handler_func(message)
            logger.info(f"[CommandHandler] Successfully handled command '{command_name}'. Result: {result}")
        except Exception as e:
            logger.exception(f"[CommandHandler] Error while executing handler for '{command_name}': {e}")
    else:
        logger.warning(f"[CommandHandler] No handler registered for command '{command_name}'. Message ignored.")
