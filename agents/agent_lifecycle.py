# agent_lifecycle.py

import threading
import time
import logging
from agent_registry import AgentRegistry
from agent_core import Agent
from plugin_loader import load_plugins

class AgentLifecycleManager:
    def __init__(self, monitor_interval=10):
        """
        Initializes the lifecycle manager.
        :param monitor_interval: Time interval in seconds for health checks.
        """
        self.logger = logging.getLogger("AgentLifecycle")
        self._configure_logger()
        self.registry = AgentRegistry()
        self.plugins = load_plugins()
        self.agents = {}
        self.running = False
        self.monitor_interval = monitor_interval

    def _configure_logger(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def initialize_agents(self):
        """Initialize agents from plugins and register them in the registry."""
        for plugin_name, plugin_instance in self.plugins.items():
            agent_name = plugin_name.split('_')[0]
            agent = Agent(agent_name, plugin_instance)
            self.registry.register(agent_name, agent)
            self.agents[agent_name] = agent
            self.logger.info(f"[Init] Agent '{agent_name}' initialized and registered.")

    def start(self):
        """Starts the agent lifecycle monitoring thread."""
        if not self.running:
            self.logger.info("[Lifecycle] Starting agent lifecycle manager...")
            self.running = True
            threading.Thread(target=self._monitor_agents, daemon=True).start()
        else:
            self.logger.warning("[Lifecycle] Agent lifecycle manager is already running.")

    def _monitor_agents(self):
        """Periodically logs agent activity as a basic health check."""
        while self.running:
            for name, agent in self.agents.items():
                status = getattr(agent, "status", "unknown")
                self.logger.info(f"[Monitor] Agent '{name}' is currently '{status}'.")
            time.sleep(self.monitor_interval)

    def stop(self):
        """Stops the lifecycle manager."""
        self.logger.info("[Lifecycle] Stopping agent lifecycle manager...")
        self.running = False

    def restart_agent(self, agent_name):
        """Attempts to restart a specific agent by reloading its plugin."""
        plugin_key = f"{agent_name}_plugin"
        if agent_name not in self.agents:
            self.logger.error(f"[Restart] Agent '{agent_name}' not found in current registry.")
            return

        if plugin_key not in self.plugins:
            self.logger.error(f"[Restart] Plugin for agent '{agent_name}' not found.")
            return

        try:
            plugin_class = type(self.plugins[plugin_key])
            new_plugin = plugin_class()
            new_agent = Agent(agent_name, new_plugin)
            self.agents[agent_name] = new_agent
            self.registry.register(agent_name, new_agent)
            self.logger.info(f"[Restart] Agent '{agent_name}' has been restarted.")
        except Exception as e:
            self.logger.error(f"[Restart] Failed to restart agent '{agent_name}': {e}")
