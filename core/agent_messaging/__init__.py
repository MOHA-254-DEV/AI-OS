"""
core.agent_messaging

This package provides the infrastructure for inter-agent messaging within the
autonomous AI operating system. It supports direct, broadcast, and queue-based
communication between agents, along with message serialization and handling.

Modules:
--------
- agent_protocol: Defines standardized message structure and agent communication schema.
- agent_messenger: Handles message routing, dispatching, and delivery.
- handlers: Modular message handlers (e.g., command, status, error).
- middleware (optional): For transformation, logging, or filtering of messages.

Usage Example:
--------------
    from core.agent_messaging import agent_messenger

    agent_messenger.send(
        sender="agent_alpha",
        receiver="agent_beta",
        command="status_update",
        payload={"cpu": 75, "memory": "512MB"}
    )
"""

import logging
from core.agent_messaging.agent_messenger import AgentMessenger

# Optional logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    from logging import StreamHandler
    handler = StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(handler)

logger.info("core.agent_messaging module initialized.")

# Optional: expose a shared global instance
agent_messenger = AgentMessenger()

# Clean public API
__all__ = [
    "AgentMessenger",
    "agent_messenger"
]
