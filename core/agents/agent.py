# core/agents/heartbeat.py

import psutil
import time
import logging
from typing import Optional

from core.orchestrator.load_balancer import LoadBalancer
from core.agent_queue import get_pending_task_count  # Update if the import path differs

# Setup logger
logger = logging.getLogger("AgentHeartbeat")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class HeartbeatSender:
    """
    Periodically collects agent system stats and sends them to the LoadBalancer.
    """

    def __init__(self, agent_id: str, interval: int = 10, load_balancer: Optional[LoadBalancer] = None):
        """
        Initialize heartbeat sender for a specific agent.

        Args:
            agent_id (str): Unique identifier of the agent.
            interval (int): Heartbeat interval in seconds.
            load_balancer (LoadBalancer, optional): Custom LoadBalancer instance.
        """
        self.agent_id = agent_id
        self.interval = interval
        self.lb = load_balancer or LoadBalancer()
        self._running = False

    def collect_metrics(self) -> dict:
        """
        Collect CPU, memory, and pending task queue length.

        Returns:
            dict: Metrics dictionary.
        """
        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().used / (1024 * 1024)  # Convert to MB
        queue_len = get_pending_task_count()

        return {
            "cpu": round(cpu, 2),
            "memory": round(memory, 2),
            "queue_length": queue_len
        }

    def send_heartbeat(self) -> None:
        """
        Collects metrics and sends heartbeat to LoadBalancer.
        """
        metrics = self.collect_metrics()
        self.lb.register_agent(
            self.agent_id,
            cpu_usage=metrics["cpu"],
            memory_usage=metrics["memory"],
            queue_length=metrics["queue_length"]
        )

        logger.info(
            f"[Heartbeat] Agent: {self.agent_id} | CPU: {metrics['cpu']}% | "
            f"Memory: {metrics['memory']}MB | Queue: {metrics['queue_length']}"
        )

    def run(self) -> None:
        """
        Starts the periodic heartbeat loop.
        """
        self._running = True
        logger.info(f"[Heartbeat] Started for agent '{self.agent_id}' (interval: {self.interval}s)")

        try:
            while self._running:
                self.send_heartbeat()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.warning(f"[Heartbeat] Stopped by user for agent '{self.agent_id}'.")
        except Exception as e:
            logger.exception(f"[Heartbeat] Unexpected error for agent '{self.agent_id}': {e}")

    def stop(self) -> None:
        """
        Stops the heartbeat loop.
        """
        self._running = False
        logger.info(f"[Heartbeat] Gracefully stopping heartbeat for '{self.agent_id}'.")


# Optional utility for standalone execution
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python heartbeat.py <agent_id>")
        sys.exit(1)

    agent_id_arg = sys.argv[1]
    hb = HeartbeatSender(agent_id_arg)
    hb.run()
