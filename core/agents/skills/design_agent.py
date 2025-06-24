# core/agents/skills/design_agent.py

import logging
from typing import Dict, Any
from ..base_agent import BaseAgent

# Configure logger
logger = logging.getLogger("DesignAgent")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class DesignAgent(BaseAgent):
    """
    An autonomous agent specialized in handling design-related tasks
    such as UI/UX, branding, and graphic design.

    Inherits:
        BaseAgent: Provides foundational behavior and state for autonomous agents.
    """

    def __init__(self):
        """
        Initializes the DesignAgent with a unique ID, role name, and skills.
        """
        super().__init__(
            agent_id="design01",
            role="DesignAgent",
            skills=["graphic_design", "ui_ux", "branding"]
        )
        logger.info("[DesignAgent] Initialized with skills: graphic_design, ui_ux, branding")

    def execute(self, task: Dict[str, Any]) -> str:
        """
        Executes a design-related task.

        Args:
            task (Dict[str, Any]): Dictionary containing task data. Must include a 'name' key.

        Returns:
            str: Result of the task execution.

        Raises:
            KeyError: If 'name' is missing in the task dictionary.
        """
        if "name" not in task:
            error_msg = "[DesignAgent] Task is missing required 'name' key."
            logger.error(error_msg)
            raise KeyError(error_msg)

        task_name = task["name"]
        logger.info(f"[DesignAgent] Starting execution for task: '{task_name}'")

        # Simulated task execution logic (replaceable with real implementation)
        result = f"Design successfully completed for task: '{task_name}'"

        logger.info(f"[DesignAgent] Completed task: '{task_name}'")
        return result
