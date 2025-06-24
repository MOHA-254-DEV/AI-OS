import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self, registry, load_balancer, max_threads=10):
        self.registry = registry
        self.load_balancer = load_balancer
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_threads)

    def assign_task(self, task_name, skill_required, task_duration=3, retry_on_fail=False):
        """Assigns a task to the best-suited agent."""
        agent = self.load_balancer.select_best_agent(skill_required)
        if not agent:
            msg = f"[Manager] No agent available for skill: {skill_required}"
            logger.warning(msg)
            if retry_on_fail:
                logger.info(f"[Manager] Retrying task '{task_name}' after 5 seconds...")
                time.sleep(5)
                self.assign_task(task_name, skill_required, task_duration)
            return

        def execute_task():
            try:
                agent_name = getattr(agent, 'name', f"Agent-{agent.id}")
                logger.info(f"[Manager] Assigning '{task_name}' to {agent_name}...")

                # Mark agent busy
                with self.lock:
                    new_load = max(0, agent.load + 1)
                    self.registry.update_status(agent.id, "busy", new_load)

                # Simulate execution
                time.sleep(task_duration)

                # Mark agent idle
                with self.lock:
                    new_load = max(0, agent.load - 1)
                    self.registry.update_status(agent.id, "idle", new_load)

                logger.info(f"[Manager] Task '{task_name}' completed by {agent_name}")

            except Exception as e:
                logger.exception(f"[Manager] Error running task '{task_name}' for agent {agent.name}: {str(e)}")

        self.executor.submit(execute_task)

    def shutdown(self):
        """Gracefully shuts down all agent threads."""
        logger.info("[Manager] Shutting down agent task manager...")
        self.executor.shutdown(wait=True)
        logger.info("[Manager] All tasks completed. Thread pool terminated.")
