# system/agent/agent_lifecycle_manager.py

import threading
import uuid
import time
from system.agent.agent_pool import AgentPool
from system.agent.agent_status import AgentStatusTracker
from system.agent.agent_hooks import AgentHooks

class AgentLifecycleManager:
    def __init__(self):
        self.agent_pool = AgentPool()
        self.status_tracker = AgentStatusTracker()
        self.hooks = AgentHooks()

    def start_agent(self, agent_type: str, task_payload: dict):
        agent_id = str(uuid.uuid4())
        print(f"[AgentLifecycle] Starting agent {agent_id} of type '{agent_type}'")

        def agent_thread():
            try:
                self.hooks.on_start(agent_id, agent_type, task_payload)
                agent_instance = self.agent_pool.get_or_create(agent_type, agent_id)
                self.status_tracker.update_status(agent_id, "running")
                result = agent_instance.execute(task_payload)
                self.status_tracker.update_result(agent_id, result)
                self.hooks.on_complete(agent_id, result)
            except Exception as e:
                self.status_tracker.update_status(agent_id, "error")
                self.status_tracker.log_error(agent_id, str(e))
                print(f"[AgentLifecycle] Agent {agent_id} crashed: {str(e)}")
            finally:
                self.status_tracker.update_status(agent_id, "completed")
                self.agent_pool.recycle(agent_id)

        t = threading.Thread(target=agent_thread)
        t.start()
        return agent_id

    def terminate_agent(self, agent_id: str):
        print(f"[AgentLifecycle] Terminating agent {agent_id}")
        self.status_tracker.update_status(agent_id, "terminated")
        self.agent_pool.remove(agent_id)

    def monitor_agents(self):
        print("[AgentLifecycle] Monitoring agents...")
        for agent_id in self.status_tracker.get_all_active():
            status = self.status_tracker.get_status(agent_id)
            if status == "error":
                print(f"[Monitor] Restarting crashed agent: {agent_id}")
                # Optional restart logic here
