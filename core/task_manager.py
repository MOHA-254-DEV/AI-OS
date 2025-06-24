# File: core/task_runtime/task_manager.py

import os
import json
import asyncio
from datetime import datetime
from importlib import import_module
from utils.logger import logger  # Optional if you have one

class TaskManager:
    def __init__(self, task_file="data/tasks/task_queue.json"):
        self.task_file = task_file
        self.queue = []
        os.makedirs(os.path.dirname(task_file), exist_ok=True)
        self._load_queue()

    def _load_queue(self):
        """Load tasks from persistent JSON file."""
        if os.path.exists(self.task_file):
            with open(self.task_file, "r") as f:
                self.queue = json.load(f)
        else:
            self.queue = []

    def _save_queue(self):
        """Save current queue to file."""
        with open(self.task_file, "w") as f:
            json.dump(self.queue, f, indent=2)

    def add_task(self, command: str, args=None, priority=1) -> dict:
        """Add a new task to the queue."""
        task = {
            "id": len(self.queue) + 1,
            "command": command,
            "args": args or [],
            "priority": priority,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending"
        }
        self.queue.append(task)
        self._save_queue()
        logger.info(f"[TaskManager] Added task {task['id']}: {command}")
        return task

    def cancel_task(self, task_id: int) -> dict:
        """Mark a task as cancelled."""
        for task in self.queue:
            if task["id"] == task_id:
                task["status"] = "cancelled"
                self._save_queue()
                logger.info(f"[TaskManager] Cancelled task {task_id}")
                return {"cancelled": task_id}
        logger.warning(f"[TaskManager] Task {task_id} not found to cancel.")
        return {"error": "Task not found"}

    def get_queue(self) -> list:
        """Get the task queue sorted by priority and timestamp."""
        return sorted(self.queue, key=lambda t: (-t["priority"], t["created_at"]))

    def list_status(self) -> list:
        """Return summary status of all tasks."""
        return [{"id": t["id"], "command": t["command"], "status": t["status"]} for t in self.queue]

    async def run_task(self, task: dict):
        """Run an individual task using plugin execution."""
        if task["status"] != "pending":
            return

        task["status"] = "running"
        self._save_queue()
        logger.info(f"[TaskManager] Running task {task['id']}: {task['command']}")

        try:
            # Dynamic plugin loader
            base_name = task["command"].split("_")[0]
            module_name = f"plugins.{base_name}_plugin"
            plugin_module = import_module(module_name)
            plugin = plugin_module.register()

            # Task handler lookup
            handler = plugin.get(task["command"])
            if not handler:
                raise ValueError(f"No handler found for command: {task['command']}")

            # Run handler (assumed to be async)
            result = await handler(task["args"])
            task["result"] = result
            task["status"] = "complete"
            logger.info(f"[TaskManager] Task {task['id']} complete.")

        except Exception as e:
            task["status"] = "error"
            task["error"] = str(e)
            logger.error(f"[TaskManager] Task {task['id']} failed: {e}")

        finally:
            self._save_queue()

    async def run_all(self):
        """Run all tasks in the queue that are still pending."""
        for task in self.get_queue():
            if task["status"] == "pending":
                await self.run_task(task)
