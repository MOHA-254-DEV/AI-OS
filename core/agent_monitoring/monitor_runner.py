"""
monitor_runner.py

Coordinates agent health monitoring and crash recovery.
Spawns background threads that periodically check agent status and initiate recovery if needed.
"""

import threading
import time
import logging

from core.agent_monitoring.health_monitor import health_monitor
from core.agent_monitoring.crash_recovery import crash_recovery
from core.task_delegation.agent_registry import agent_registry

# Set up logger
logger = logging.getLogger("MonitorRunner")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class MonitorRunner:
    """
    Starts and coordinates continuous background threads for:
    - Health monitoring (CPU/memory/heartbeat)
    - Crash detection and recovery
    """

    def __init__(self):
        # Load list of agent IDs from registry
        self.agents = list(agent_registry.agents.keys())
        logger.info(f"[MonitorRunner] Initialized with {len(self.agents)} agent(s).")

    def start(self):
        """
        Starts the monitoring and crash recovery loops in background threads.
        """
        if not self.agents:
            logger.warning("[MonitorRunner] No agents to monitor. Start aborted.")
            return

        # Thread for health monitoring
        health_thread = threading.Thread(
            target=health_monitor.run,
            args=(self.agents,),
            daemon=True,
            name="HealthMonitorThread"
        )

        # Thread for crash recovery
        crash_thread = threading.Thread(
            target=self._crash_loop,
            daemon=True,
            name="CrashRecoveryThread"
        )

        health_thread.start()
        crash_thread.start()

        logger.info("[MonitorRunner] Monitoring and recovery threads started.")

    def _crash_loop(self):
        """
        Continuously check for crashed agents and try to recover them.
        """
        logger.info("[MonitorRunner] Crash recovery loop running...")
        while True:
            try:
                crash_recovery.detect_and_recover()
                time.sleep(5)  # Adjustable interval
            except Exception as e:
                logger.exception(f"[MonitorRunner] Error during crash recovery loop: {e}")


# Singleton instance exposed globally
monitor_runner = MonitorRunner()
