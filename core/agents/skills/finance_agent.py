# core/agents/skills/finance_agent.py

import logging
from typing import Dict, Any
from ..base_agent import BaseAgent

# Configure logger specifically for FinanceAgent
logger = logging.getLogger("FinanceAgent")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class FinanceAgent(BaseAgent):
    """
    Autonomous agent for financial tasks:
    - Trading and investment simulations
    - Accounting computations
    - Financial data analytics
    """

    def __init__(self):
        """
        Initialize the FinanceAgent with ID, role, and relevant skills.
        """
        super().__init__(
            agent_id="finance01",
            role="FinanceAgent",
            skills=["trading", "accounting", "analytics"]
        )
        logger.info("[FinanceAgent] Initialized with skills: trading, accounting, analytics")

    def execute(self, task: Dict[str, Any]) -> str:
        """
        Execute a financial task provided in the task dictionary.

        Args:
            task (Dict[str, Any]): Must include 'name' representing the task's title.

        Returns:
            str: Result message after completing the task.

        Raises:
            KeyError: If task does not include 'name'.
        """
        if "name" not in task:
            error_msg = "[FinanceAgent] Task dictionary is missing the 'name' key."
            logger.error(error_msg)
            raise KeyError(error_msg)

        task_name = task["name"]
        logger.info(f"[FinanceAgent] Executing finance task: '{task_name}'")

        # Placeholder logic for future financial algorithm integration
        result = f"Finance insights generated for '{task_name}'"

        logger.info(f"[FinanceAgent] Task completed: '{task_name}'")
        return result
