# agent_manager/agent_registry.py

import logging
from typing import Dict, Optional, Any, List

class AgentRegistry:
    def __init__(self):
        """
        Manages a collection of named agents.
        """
        self.agents: Dict[str, Any] = {}
        self.logger = logging.getLogger("AgentRegistry")
        self._setup_logger()

    def _setup_logger(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def register(self, name: str, agent: Any):
        """
        Registers an agent instance with a unique name.

        :param name: Unique name to identify the agent.
        :param agent: The agent instance (should conform to expected interface).
        """
        if name in self.agents:
            self.logger.warning(f"⚠️ Agent '{name}' is already registered. Overwriting.")
        self.agents[name] = agent
        self.logger.info(f"✅ Agent '{name}' registered successfully.")

    def get(self, name: str) -> Optional[Any]:
        """
        Fetches a registered agent by name.

        :param name: Name of the agent.
        :return: The agent instance or None.
        """
        agent = self.agents.get(name)
        if agent:
            self.logger.info(f"📦 Retrieved agent '{name}'.")
        else:
            self.logger.warning(f"❌ Agent '{name}' not found.")
        return agent

    def list_agents(self) -> List[str]:
        """
        Lists all currently registered agent names.

        :return: List of agent names.
        """
        names = list(self.agents.keys())
        if names:
            self.logger.info(f"🗂️ Registered agents: {', '.join(names)}")
        else:
            self.logger.info("🗃️ No agents registered.")
        return names

    def unregister(self, name: str):
        """
        Unregisters and removes an agent by name.

        :param name: Name of the agent to remove.
        """
        if name in self.agents:
            del self.agents[name]
            self.logger.info(f"🗑️ Agent '{name}' unregistered successfully.")
        else:
            self.logger.warning(f"⚠️ Cannot unregister: Agent '{name}' not found.")
