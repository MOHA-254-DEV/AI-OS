# core/agent_state/state_registry.py

import logging
from threading import Lock
from datetime import datetime
from typing import Dict, Optional, Any

from .state_models import AgentState

# Configure logger
logger = logging.getLogger("AgentStateRegistry")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class AgentStateNotFoundException(Exception):
    """Raised when the requested agent state is not found in the registry."""
    pass


class AgentStateRegistry:
    """
    Thread-safe in-memory registry of agent states.
    Handles registering, updating, and retrieving current agent information.
    """
    def __init__(self):
        self._states: Dict[str, AgentState] = {}
        self._lock = Lock()

    def register_agent(self, state: AgentState) -> None:
        """
        Registers or updates an agent's full state object.

        Args:
            state (AgentState): The full state snapshot to store.
        """
        with self._lock:
            self._states[state.agent_id] = state
            logger.info(f"[AgentStateRegistry] Registered or updated agent: {state.agent_id}")

    def update_state(self, agent_id: str, field: str, value: Any, timestamp: datetime) -> None:
        """
        Updates a specific field of an agent's state if the field exists.

        Args:
            agent_id (str): ID of the agent.
            field (str): Field name to update (must exist on AgentState).
            value (Any): New value to assign.
            timestamp (datetime): Time of update.

        Raises:
            AgentStateNotFoundException: If the agent is not registered.
            AttributeError: If the specified field does not exist.
        """
        with self._lock:
            current = self._states.get(agent_id)
            if not current:
                raise AgentStateNotFoundException(f"No state found for agent '{agent_id}'")

            if not hasattr(current, field):
                raise AttributeError(f"Field '{field}' not found on AgentState model.")

            setattr(current, field, value)
            current.timestamp = timestamp
            logger.debug(f"[AgentStateRegistry] Updated '{agent_id}.{field}' to '{value}' at {timestamp}")

    def get_state(self, agent_id: str) -> Optional[AgentState]:
        """
        Fetch the current state of a specific agent.

        Args:
            agent_id (str): The agent's unique identifier.

        Returns:
            Optional[AgentState]: The agent's state if available.
        """
        with self._lock:
            return self._states.get(agent_id)

    def all_states(self) -> Dict[str, AgentState]:
        """
        Retrieve a snapshot of all agent states.

        Returns:
            Dict[str, AgentState]: A copy of the internal state dictionary.
        """
        with self._lock:
            return self._states.copy()
