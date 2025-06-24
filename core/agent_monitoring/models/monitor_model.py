"""
monitor_model.py

Enhanced model for agent health tracking.
This version includes simple accessors, better logging, extended agent metadata,
and pruning feedback.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import time
import threading
import logging

# Logger setup
logger = logging.getLogger("HealthRegistry")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

@dataclass
class AgentHealth:
    """
    Keeps track of how healthy an agent is.
    Includes CPU, memory usage, uptime, and last time the agent checked in.
    """
    agent_id: str
    last_heartbeat: float
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    start_time: float = field(default_factory=time.time)
    custom_tags: Dict[str, str] = field(default_factory=dict)

    @property
    def uptime(self) -> float:
        """How long the agent has been alive (in seconds)."""
        return round(time.time() - self.start_time, 2)

    def to_dict(self) -> Dict:
        """Convert health data to dictionary form."""
        return {
            "agent_id": self.agent_id,
            "last_heartbeat": self.last_heartbeat,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "uptime": self.uptime,
            "custom_tags": self.custom_tags
        }

class HealthRegistry:
    """
    Central service to keep track of all agents' health.
    Thread-safe and provides updating, removing, fetching, and cleaning.
    """
    def __init__(self):
        self._registry: Dict[str, AgentHealth] = {}
        self._lock = threading.Lock()

    def update_heartbeat(self, agent_id: str, cpu: float, memory: float, tags: Optional[Dict[str, str]] = None):
        """
        Called when an agent sends a heartbeat.
        Records CPU, memory, and optionally custom tags.
        """
        now = time.time()
        with self._lock:
            if agent_id not in self._registry:
                self._registry[agent_id] = AgentHealth(
                    agent_id=agent_id,
                    last_heartbeat=now,
                    cpu_usage=cpu,
                    memory_usage=memory,
                    custom_tags=tags or {}
                )
                logger.info(f"[HealthRegistry] Registered new agent '{agent_id}'")
            else:
                agent = self._registry[agent_id]
                agent.last_heartbeat = now
                agent.cpu_usage = cpu
                agent.memory_usage = memory
                if tags:
                    agent.custom_tags.update(tags)
                logger.debug(f"[HealthRegistry] Updated heartbeat for agent '{agent_id}'")

    def get_health(self, agent_id: str) -> Optional[AgentHealth]:
        """Returns a single agent's health info."""
        with self._lock:
            return self._registry.get(agent_id)

    def get_all_health(self) -> Dict[str, Dict]:
        """Returns health info for all agents as dicts."""
        with self._lock:
            return {aid: agent.to_dict() for aid, agent in self._registry.items()}

    def remove_agent(self, agent_id: str) -> bool:
        """Manually remove an agent from registry."""
        with self._lock:
            if agent_id in self._registry:
                del self._registry[agent_id]
                logger.info(f"[HealthRegistry] Agent '{agent_id}' removed.")
                return True
            return False

    def prune_inactive_agents(self, timeout_seconds: float) -> int:
        """
        Deletes agents who haven’t pinged in a while.
        Returns number of agents removed.
        """
        now = time.time()
        removed = []
        with self._lock:
            for aid, health in list(self._registry.items()):
                if now - health.last_heartbeat > timeout_seconds:
                    del self._registry[aid]
                    removed.append(aid)
        for aid in removed:
            logger.warning(f"[HealthRegistry] Pruned inactive agent '{aid}' after {timeout_seconds}s timeout.")
        return len(removed)

    def is_active(self, agent_id: str, threshold: float = 30.0) -> bool:
        """
        Check if an agent is active within the last X seconds.
        """
        agent = self.get_health(agent_id)
        if not agent:
            return False
        return (time.time() - agent.last_heartbeat) <= threshold


# ✅ Singleton instance
health_registry = HealthRegistry()
