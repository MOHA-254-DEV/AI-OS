# /core/agent_messaging/handlers/status_handler.py

import logging
from datetime import datetime
from core.agent_messaging.agent_protocol import AgentMessage

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    from logging import StreamHandler
    handler = StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def handle(message: AgentMessage) -> None:
    """
    Handles status-type messages from agents.

    Parameters:
    - message (AgentMessage): The message object containing sender and payload data.
    """
    if not isinstance(message, AgentMessage):
        logger.error("[StatusHandler] Invalid message format received.")
        return

    timestamp = datetime.utcnow().isoformat()
    logger.info(f"[StatusHandler] [{timestamp}] Status received from '{message.sender}': {message.payload}")

    # Optional: Additional processing logic (forward to dashboard, trigger health check, etc.)
    # forward_to_monitoring_service(message)
