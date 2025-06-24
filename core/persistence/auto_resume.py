# File: core/persistence/auto_resume.py

import os
from .state_manager import StateManager
from core.agent.agent_registry import AgentRegistry
from core.agent.agent_executor import AgentExecutor
from core.logging.plugin_logger import PluginLogger

class AutoResume:
    def __init__(self):
        self.registry = AgentRegistry()
        self.logger = PluginLogger()

    def resume_all(self):
        """
        Resume all agents that have saved state from a previous session.
        """
        agent_ids = self.registry.get_all_agent_ids()
        for agent_id in agent_ids:
            try:
                state_mgr = StateManager(agent_id)
                if not state_mgr.has_state():
                    continue

                state = state_mgr.load_state()
                print(f"[AutoResume] Resuming agent {agent_id}...")
                executor = AgentExecutor(agent_id)
                executor.resume_from_state(state)

                self.logger.log(
                    plugin_name="AutoResume",
                    input_code=f"Resumed agent {agent_id}",
                    output="Execution resumed from last known state",
                    success=True,
                    metadata={"state_snapshot": state}
                )

            except Exception as e:
                self.logger.log(
                    plugin_name="AutoResume",
                    input_code=f"Error resuming agent {agent_id}",
                    output="Resume failed",
                    success=False,
                    error=str(e)
                )
