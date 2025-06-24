# /core/task_delegation/agent_registry.py

from typing import Dict, List, Optional
from threading import Lock


class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, Dict] = {}
        self.lock = Lock()

    def register_agent(self, agent_id: str, skills: List[str], status: str = "idle"):
        with self.lock:
            self.agents[agent_id] = {
                "skills": skills,
                "status": status,
                "tasks": []
            }

    def update_status(self, agent_id: str, status: str):
        with self.lock:
            if agent_id in self.agents:
                self.agents[agent_id]["status"] = status

    def assign_task(self, agent_id: str, task_id: str):
        with self.lock:
            if agent_id in self.agents:
                if task_id not in self.agents[agent_id]["tasks"]:
                    self.agents[agent_id]["tasks"].append(task_id)
                    self.agents[agent_id]["status"] = "busy"

    def get_idle_agents_with_skill(self, skill: str) -> List[str]:
        with self.lock:
            return [
                aid for aid, data in self.agents.items()
                if skill in data["skills"] and data["status"] == "idle"
            ]

    def deregister_agent(self, agent_id: str):
        with self.lock:
            if agent_id in self.agents:
                del self.agents[agent_id]

    def get_agent(self, agent_id: str) -> Optional[Dict]:
        return self.agents.get(agent_id)

    def list_agents(self) -> Dict[str, Dict]:
        return self.agents.copy()


# Singleton instance
agent_registry = AgentRegistry()
