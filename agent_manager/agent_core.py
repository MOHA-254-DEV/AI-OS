# agent_manager/agent_core.py

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AgentCore:
    def __init__(self):
        self.agents = {}
        self.status = "initialized"
        logger.info("AgentCore initialized")
        
    def register_agent(self, agent_id: str, agent_config: Dict[str, Any]):
        """Register a new agent"""
        self.agents[agent_id] = agent_config
        logger.info(f"Agent {agent_id} registered")
        
    def get_agent_status(self, agent_id: str):
        """Get status of specific agent"""
        return self.agents.get(agent_id, {}).get("status", "unknown")


class Agent:
    def __init__(self, name: str, plugin: Any):
        """
        Represents an autonomous agent that handles tasks using a specific plugin.

        :param name: The name of the agent.
        :param plugin: An instance of a Plugin that defines task logic.
        """
        self.name = name
        self.plugin = plugin
        self.status = "idle"
        self.logger = logging.getLogger(f"Agent-{self.name}")
        self._setup_logger()

    def _setup_logger(self):
        """Configures logging for this agent."""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_task_start(self, task_name: str):
        """Logs the beginning of a task."""
        self.logger.info(f"🚀 Starting task: '{task_name}'")

    def log_task_end(self, task_name: str, success: bool = True):
        """Logs the result of a task."""
        status = "✅ completed successfully" if success else "❌ failed"
        self.logger.info(f"🏁 Task '{task_name}' {status}")

    def handle_task(self, task: Dict[str, Any]) -> str:
        """
        Executes a task using the agent's plugin.

        :param task: A dictionary containing task metadata and payload (under 'data').
        :return: A string describing the outcome of the task.
        """
        task_name = task.get("task_name", "Unnamed Task")

        try:
            if not isinstance(task, dict) or "data" not in task:
                raise ValueError("Invalid task structure. Missing 'data' field.")

            self.status = "busy"
            self.log_task_start(task_name)

            # Execute plugin's task handler
            result = self.plugin.run(task["data"])

            self.status = "idle"
            self.log_task_end(task_name, success=True)

            return f"Agent[{self.name}] ✅ completed task '{task_name}': {result}"

        except Exception as e:
            self.status = "idle"
            self.log_task_end(task_name, success=False)
            self.logger.error(f"❌ Error while processing task '{task_name}': {e}")
            return f"Agent[{self.name}] ❌ failed to complete task '{task_name}': {e}"
