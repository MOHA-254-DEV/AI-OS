# agent_coordinator/load_balancer.py

import logging
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agent_coordinator.registry import Agent  # Avoid circular import during runtime

# Configure structured logger
logger = logging.getLogger("AgentLoadBalancer")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class LoadBalancer:
    def __init__(self, registry):
        """
        Initialize the load balancer with an agent registry.
        The registry must implement `get_all_agents()`.
        """
        if not hasattr(registry, "get_all_agents"):
            raise ValueError("Registry must implement get_all_agents() method.")
        self.registry = registry

    def select_best_agent(self, required_skill: str) -> Optional["Agent"]:
        """
        Selects a single best agent with the required skill who is currently idle and has the lowest load.

        :param required_skill: The skill required for the task.
        :return: An Agent object or None.
        """
        try:
            agents = self.registry.get_all_agents()
        except Exception as e:
            logger.error(f"Failed to retrieve agents: {e}")
            return None

        candidates = [a for a in agents if self._is_valid_agent(a, required_skill)]

        if not candidates:
            logger.warning(f"No available agents with skill '{required_skill}'")
            return None

        best_agent = min(candidates, key=lambda a: getattr(a, "load", float('inf')))
        logger.info(f"Selected agent '{best_agent.name}' (ID: {best_agent.id}) with load {best_agent.load} for skill '{required_skill}'")
        return best_agent

    def _is_valid_agent(self, agent: "Agent", required_skill: str) -> bool:
        """
        Check if an agent is idle and has the required skill.

        :param agent: The agent to evaluate.
        :param required_skill: The skill string.
        :return: True if agent qualifies.
        """
        try:
            return (
                required_skill in getattr(agent, "skills", []) and
                getattr(agent, "status", "") == "idle"
            )
        except Exception as e:
            logger.error(f"Invalid agent encountered during skill check: {e}")
            return False

    def select_best_agents(self, required_skills: List[str], limit: int = 3) -> List["Agent"]:
        """
        Selects the top N agents that match all required skills and are idle.

        :param required_skills: List of required skills.
        :param limit: Max number of agents to return.
        :return: List of agent objects.
        """
        try:
            agents = self.registry.get_all_agents()
        except Exception as e:
            logger.error(f"Failed to retrieve agents: {e}")
            return []

        candidates = [
            agent for agent in agents
            if self._has_all_skills(agent, required_skills) and getattr(agent, "status", "") == "idle"
        ]

        sorted_candidates = sorted(candidates, key=lambda a: getattr(a, "load", float('inf')))
        selected = sorted_candidates[:limit]
        logger.info(f"Selected {len(selected)} agents for skills {required_skills}")
        return selected

    def _has_all_skills(self, agent: "Agent", skills: List[str]) -> bool:
        """
        Check if an agent has all required skills.

        :param agent: The agent to check.
        :param skills: List of required skills.
        :return: True if agent has all skills.
        """
        try:
            agent_skills = set(getattr(agent, "skills", []))
            return all(skill in agent_skills for skill in skills)
        except Exception as e:
            logger.error(f"Skill check failed for agent {getattr(agent, 'name', '?')}: {e}")
            return False
