# agent_manager/task_delegator.py

import logging

class TaskDelegator:
    def __init__(self, registry):
        self.registry = registry
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def delegate(self, task):
        """
        Delegates the task to an agent based on task['type'].

        :param task: A dictionary with at least the key 'type' and 'data'
        :return: Result of task execution or error message
        """
        if not isinstance(task, dict) or 'type' not in task:
            self.logger.error("Task missing 'type' key or is not a dictionary.")
            return "[ERROR] Invalid task format. Must include a 'type' field."

        task_type = task["type"]
        self.logger.info(f"🔍 Delegating task of type: {task_type}")

        agent = self.registry.get(task_type)

        if not agent:
            self.logger.warning(f"No registered agent found for type: {task_type}")
            return f"[ERROR] No agent found for task type: '{task_type}'."

        try:
            result = agent.handle_task(task)
            self.logger.info(f"✅ Task of type '{task_type}' executed successfully.")
            return result
        except Exception as e:
            self.logger.exception(f"❌ Failed to execute task '{task_type}': {e}")
            return f"[ERROR] Failed to execute task '{task_type}': {str(e)}"
