"""
conflict_resolver.py

Handles detection and resolution of state conflicts between agents.
Ensures updates are applied only if newer than the current state.
"""

from typing import List
from datetime import datetime
import logging

from .state_registry import AgentStateRegistry
from .state_models import AgentState, StateUpdate

# Setup logger
logger = logging.getLogger("ConflictResolver")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ConflictResolver:
    """
    Ensures agent state updates are applied only if they're newer than what's already stored.
    """

    def __init__(self, registry: AgentStateRegistry):
        """
        :param registry: An instance of AgentStateRegistry managing agent state objects.
        """
        self.registry = registry

    def detect_conflicts(self, updates: List[StateUpdate]) -> List[StateUpdate]:
        """
        Detects which updates are outdated compared to current state data.

        :param updates: List of incoming state updates.
        :return: List of updates that are in conflict (i.e., outdated).
        """
        conflicts = []

        for update in updates:
            current_state = self.registry.get_state(update.agent_id)
            if current_state:
                current_value = getattr(current_state, update.field, None)
                if current_value != update.new_value:
                    if current_state.timestamp > update.timestamp:
                        logger.warning(
                            f"[Conflict] Agent '{update.agent_id}', field '{update.field}': "
                            f"local is newer (local={current_state.timestamp}, update={update.timestamp})"
                        )
                        conflicts.append(update)

        return conflicts

    def resolve_conflicts(self, updates: List[StateUpdate]) -> None:
        """
        Resolves and applies only valid (newer) updates.

        :param updates: List of updates to apply.
        """
        for update in updates:
            current_state = self.registry.get_state(update.agent_id)

            if not current_state:
                logger.warning(
                    f"[Resolver] No existing state found for agent '{update.agent_id}'. Skipping."
                )
                continue

            if update.timestamp > current_state.timestamp:
                self.registry.update_state(
                    agent_id=update.agent_id,
                    field=update.field,
                    new_value=update.new_value,
                    timestamp=update.timestamp
                )
                logger.info(
                    f"[Resolver] Updated '{update.agent_id}.{update.field}' → '{update.new_value}' @ {update.timestamp}"
                )
            else:
                logger.debug(
                    f"[Resolver] Skipped outdated update for '{update.agent_id}.{update.field}' "
                    f"(current={current_state.timestamp}, update={update.timestamp})"
                )
