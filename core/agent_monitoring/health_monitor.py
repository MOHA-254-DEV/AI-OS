"""
health_monitor.py

Tracks real-time health metrics for each agent (CPU %, memory %) and reports them to a central registry.
Runs in a loop, periodically updating heartbeats for all monitored agents.
"""

import psutil
import time
import logging
from typing import List

from core.agent_monitoring.models.monitor_model import health_registry

# Initialize logging
logger = logging.getLogger("HealthMonitor")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class HealthMonitor:
    """
    Monitors CPU and memory usage of agents and sends heartbeat updates to the health registry.
    """

    def __init__(self, interval: int = 5):
        """
        :param interval: Interval (in seconds) between heartbeat updates.
        """
        self.interval = interval

    def heartbeat(self, agent_id: str):
        """
        Capture CPU and memory usage and update heartbeat for a specific agent.

        :param agent_id: The unique identifier for the agent.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            memory_usage = psutil.virtual_memory().percent

            health_registry.update_heartbeat(agent_id, cpu=cpu_usage, memory=memory_usage)

            logger.debug(
                f"[HealthMonitor] Heartbeat updated for agent '{agent_id}' | "
                f"CPU: {cpu_usage:.2f}%, Memory: {memory_usage:.2f}%"
            )
        except Exception as e:
            logger.exception(f"[HealthMonitor] Failed to update heartbeat for agent '{agent_id}': {e}")

    def run(self, agent_ids: List[str]):
        """
        Start continuous monitoring of agent health.

        :param agent_ids: List of agent IDs to monitor.
        """
        if not agent_ids:
            logger.warning("[HealthMonitor] No agents provided to monitor.")
            return

        logger.info(f"[HealthMonitor] Starting with {len(agent_ids)} agent(s). Interval = {self.interval}s")

        try:
            while True:
                for agent_id in agent_ids:
                    self.heartbeat(agent_id)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("[HealthMonitor] Stopped by user (KeyboardInterrupt).")
        except Exception as e:
            logger.exception(f"[HealthMonitor] Error during monitoring loop: {e}")


# Global instance (singleton)
health_monitor = HealthMonitor()
