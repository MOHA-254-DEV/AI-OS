"""
crash_recovery.py

Crash recovery logic for autonomous agents.

This module continuously scans the agent health registry and triggers recovery 
for agents that have not sent heartbeats within a defined timeout window.
"""

import time
import logging
from typing import List, Tuple

from core.agent_monitoring.models.monitor_model import health_registry
from core.task_delegation.agent_registry import agent_registry

# Configure logging
logger = logging.getLogger("CrashRecovery")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class CrashRecovery:
    """
    Detects and recovers crashed agents by checking missed heartbeats.
    """

    def __init__(self, timeout: int = 15):
        """
        :param timeout: Seconds to wait before considering an agent as unresponsive.
        """
        self.timeout = timeout
        self.recovery_log: List[Tuple[str, float]] = []

    def detect_and_recover(self):
        """
        Main recovery loop. Scans the health registry and recovers agents that missed the heartbeat deadline.
        """
        now = time.time()
        logger.debug("[CrashRecovery] Scanning for failed agents...")

        all_health = health_registry.get_all()

        for agent_id, health in all_health.items():
            time_since_last_heartbeat = now - health.last_heartbeat

            if time_since_last_heartbeat > self.timeout:
                logger.warning(
                    f"[CrashRecovery] Agent '{agent_id}' unresponsive "
                    f"(last seen {time_since_last_heartbeat:.2f}s ago)"
                )
                self.restart_agent(agent_id)

    def restart_agent(self, agent_id: str):
        """
        Attempts to restart an unresponsive agent by resetting its status and heartbeat.

        :param agent_id: ID of the agent to restart.
        """
        agent = agent_registry.agents.get(agent_id)

        if not agent:
            logger.error(f"[CrashRecovery] Agent '{agent_id}' not found in registry.")
            return

        try:
            # Update simulated agent status
            agent["status"] = "restarted"

            # Reset heartbeat with zero resource usage
            health_registry.update_heartbeat(agent_id, cpu=0.0, memory=0.0)

            # Log the recovery
            recovery_time = time.time()
            self.recovery_log.append((agent_id, recovery_time))

            logger.info(f"[CrashRecovery] Agent '{agent_id}' successfully recovered at {time.ctime(recovery_time)}.")

        except Exception as e:
            logger.exception(f"[CrashRecovery] Failed to restart agent '{agent_id}': {e}")


# Singleton instance (used by monitor runner or health check manager)
crash_recovery = CrashRecovery()
