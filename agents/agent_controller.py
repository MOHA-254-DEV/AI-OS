# agent_controller.py

import logging
from agent_registry import AgentRegistry
from task_delegator import TaskDelegator
from plugin_loader import load_plugins
from agent_core import Agent  # Ensure this is imported

class AgentController:
    def __init__(self):
        # Logger setup
        self.logger = logging.getLogger("AgentController")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # Load plugins and register agents
        self.plugins = load_plugins()
        self.registry = AgentRegistry()
        self._register_agents()

        # Create the task delegator
        self.delegator = TaskDelegator(self.registry)

    def _register_agents(self):
        """ Registers all agents based on loaded plugins """
        for plugin_name, plugin_instance in self.plugins.items():
            agent_name = plugin_name.split('_')[0]
            agent = Agent(agent_name, plugin_instance)
            self.registry.register(agent_name, agent)
            self.logger.info(f"[Controller] Registered agent: {agent_name}")

    def delegate_task(self, task: dict) -> dict:
        """
        Delegates a task to the appropriate agent.

        :param task: Task dictionary with 'type' and 'data'
        :return: Result dictionary
        """
        self.logger.info(f"[Controller] Delegating task of type: {task.get('type')}")
        return self.delegator.delegate(task)

    def start(self):
        """ Start the controller """
        self.logger.info("[Controller] Agent Controller started.")
        # In production, connect this to a queue or trigger source.

    def stop(self):
        """ Stop the controller and clean up """
        self.logger.info("[Controller] Agent Controller stopped.")
        # Add cleanup logic if needed
