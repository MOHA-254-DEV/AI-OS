# core/agents/agent_registry.py

import logging
from typing import Optional, List, Dict
from .skills.design_agent import DesignAgent
from .skills.marketing_agent import MarketingAgent
from .skills.dev_agent import DevAgent
from .skills.finance_agent import FinanceAgent
from .base_agent import BaseAgent

# Configure logger
logger = logging.getLogger("AgentRegistry")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class AgentRegistry:
    """
    Central registry that manages all active AI agents in the system.
    Supports registration, lookup by skill, and agent listings.
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}  # agent_id → BaseAgent
        self._skill_index: Dict[str, List[str]] = {}  # skill → [agent_id]
        self._register_all()

    def _register_agent(self, agent: BaseAgent):
        """
        Registers an individual agent and indexes its skills.

        Args:
            agent (BaseAgent): The agent to register.
        """
        if agent.agent_id in self.agents:
            logger.warning(f"Agent '{agent.agent_id}' is already registered.")
            return

        self.agents[agent.agent_id] = agent
        for skill in agent.skills:
            self._skill_index.setdefault(skill, []).append(agent.agent_id)

        logger.info(f"[AgentRegistry] Registered agent '{agent.agent_id}' with skills: {agent.skills}")

    def _register_all(self):
        """
        Instantiates and registers all predefined agent classes.
        """
        agent_classes = [DesignAgent, MarketingAgent, DevAgent, FinanceAgent]
        for cls in agent_classes:
            try:
                agent = cls()
                self._register_agent(agent)
            except Exception as e:
                logger.error(f"Failed to register agent from class {cls.__name__}: {e}")

    def get_agent(self, task_type: str) -> Optional[BaseAgent]:
        """
        Returns the first available agent that can handle a specific skill/task type.

        Args:
            task_type (str): The task skill/category required.

        Returns:
            Optional[BaseAgent]: A matching agent or None if no capable agent exists.
        """
        candidate_ids = self._skill_index.get(task_type.lower(), [])
        for agent_id in candidate_ids:
            agent = self.agents.get(agent_id)
            if agent and agent.can_handle(task_type):
                logger.info(f"[AgentRegistry] Selected agent '{agent.agent_name}' for task '{task_type}'")
                return agent

        logger.warning(f"[AgentRegistry] No agent available for task type '{task_type}'")
        return None

    def list_agents(self) -> List[str]:
        """
        Returns a list of all registered agent IDs.
        """
        return list(self.agents.keys())

    def get_agent_by_id(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Retrieve an agent directly by its unique ID.

        Args:
            agent_id (str): The unique identifier for the agent.

        Returns:
            Optional[BaseAgent]: The agent if found, else None.
        """
        return self.agents.get(agent_id)

    def get_agents_by_skill(self, skill: str) -> List[BaseAgent]:
        """
        Returns a list of agents that have the specified skill.

        Args:
            skill (str): The skill to filter agents by.

        Returns:
            List[BaseAgent]: Agents matching the skill.
        """
        agent_ids = self._skill_index.get(skill.lower(), [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]

# Global instance
agent_registry = AgentRegistry()
