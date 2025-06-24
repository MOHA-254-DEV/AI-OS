# core/agents/skills/dev_agent.py

import logging
from typing import Dict, Any
from ..base_agent import BaseAgent

# Configure logger for development agent
logger = logging.getLogger("DevAgent")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class DevAgent(BaseAgent):
    """
    An autonomous agent specialized in development tasks such as:
    - Full-stack application development
    - API engineering
    - Network configuration

    Inherits:
        BaseAgent: Abstract base class for all autonomous agents.
    """

    def __init__(self):
        """
        Initializes the DevAgent with its unique ID, role label, and relevant skills.
        """
        super().__init__(
            agent_id="dev01",
            role="DevAgent",
            skills=["full_stack", "api_dev", "networking"]
        )
        logger.info("[DevAgent] Initialized with skills: full_stack, api_dev, networking")

    def execute(self, task: Dict[str, Any]) -> str:
        """
        Executes a development task. Logs task and returns status message.

        Args:
            task (Dict[str, Any]): The task to execute. Must contain a 'name' key.

        Returns:
            str: A string indicating task result.

        Raises:
            KeyError: If the task doesn't contain the 'name' field.
        """
        if "name" not in task:
            error_msg = "[DevAgent] Task is missing required 'name' key."
            logger.error(error_msg)
            raise KeyError(error_msg)

        task_name = task["name"]
        logger.info(f"[DevAgent] Executing development task: '{task_name}'")

        # Placeholder for actual development task logic
        result = f"Development completed for task: '{task_name}'"

        logger.info(f"[DevAgent] Task completed: '{task_name}'")
        return result
