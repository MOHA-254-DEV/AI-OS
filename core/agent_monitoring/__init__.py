"""
agent_monitoring.__init__.py

Initializes the agent monitoring subsystem.

Exposes:
- monitor_runner: the singleton instance responsible for monitoring agent health (heartbeats, CPU, memory).
"""

from .monitor_runner import monitor_runner

# Optional logging on init
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    import sys
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.info("[agent_monitoring] Monitoring subsystem initialized. Runner is ready.")

__all__ = ["monitor_runner"]
