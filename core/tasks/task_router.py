# core/tasks/task_router.py

import logging
from core.agents.agent_registry import AgentRegistry

class TaskRouter:
    def __init__(self):
        self.registry = AgentRegistry()

    def route_task(self, task):
        task_type = task.get("type")
        if not task_type:
            raise ValueError("Task must include a 'type' field.")

        candidates = self.registry.get_agents_by_skill(task_type)

        if not candidates:
            logging.warning(f"[Router] No available agents for task type: {task_type}")
            return None

        # TODO: Could use least-loaded, round-robin, or predictive here
        selected_agent = candidates[0]

        logging.info(f"[Router] Task '{task['name']}' routed to agent: {selected_agent.agent_id}")
        return selected_agent
