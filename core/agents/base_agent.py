# core/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
import uuid
from datetime import datetime


logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Provides common interface and logic for agent metadata, capabilities, and task execution.
    """

    def __init__(self, agent_id: str, agent_name: str, skills: List[str]):
        """
        Initialize the base agent.

        Args:
            agent_id (str): Unique identifier for the agent.
            agent_name (str): Human-readable name.
            skills (List[str]): Capabilities of the agent.
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_name = agent_name
        self.skills = skills
        self.created_at = datetime.utcnow()

        logger.info(f"[{self.agent_name}] Initialized with skills: {self.skills}")

    def can_handle(self, task_type: str) -> bool:
        """
        Check if this agent can handle a specific task type.

        Args:
            task_type (str): Task skill/domain.

        Returns:
            bool: True if agent has the skill.
        """
        result = task_type.lower() in [skill.lower() for skill in self.skills]
        logger.debug(f"[{self.agent_name}] Can handle '{task_type}': {result}")
        return result

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> str:
        """
        Execute a task — must be implemented by subclasses.

        Args:
            task (Dict[str, Any]): Task description.

        Returns:
            str: Outcome/result string.
        """
        pass

    def describe(self) -> Dict[str, Any]:
        """
        Returns a description of the agent's identity and capabilities.

        Returns:
            Dict[str, Any]: Agent metadata.
        """
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "skills": self.skills,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<{self.agent_name} ({self.agent_id}) | Skills: {', '.join(self.skills)}>"
