# core/tasks/task_dispatcher.py

import logging
from core.tasks.task_router import TaskRouter
from core.agent.agent_registry import agent_registry

logging.basicConfig(
    filename='core/logs/execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TaskDispatcher:
    def __init__(self):
        self.router = TaskRouter()

    def dispatch(self, task: dict):
        try:
            # Route task to best agent (by ID)
            agent_id = self.router.route_task(task)
            if not agent_id:
                logging.warning(f"No suitable agent found for task '{task['name']}'")
                return None

            # Lookup agent object (assuming registry holds live objects or proxies)
            agent = agent_registry.agents.get(agent_id)
            if not agent or not hasattr(agent, 'execute'):
                raise ValueError(f"Agent '{agent_id}' not found or does not implement 'execute()'")

            result = agent.execute(task)

            logging.info(
                f"Task '{task['name']}' executed by {agent_id} with result: {result}"
            )
            return result

        except Exception as e:
            logging.error(
                f"Failed to dispatch task '{task.get('name', 'unknown')}': {str(e)}"
            )
            return None
