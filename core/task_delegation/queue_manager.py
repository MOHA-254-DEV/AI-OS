# /core/task_delegation/queue_manager.py
from queue import PriorityQueue
from threading import Lock
from typing import Optional, Dict

class MultiAgentQueueManager:
    def __init__(self):
        self.priority_queues = {
            "high": PriorityQueue(),
            "medium": PriorityQueue(),
            "low": PriorityQueue()
        }
        self.lock = Lock()

    def enqueue_task(self, priority: str, task_id: str, task_data: dict):
        if priority not in self.priority_queues:
            raise ValueError(f"Invalid priority level: {priority}")
        if "timestamp" not in task_data:
            raise ValueError("Missing 'timestamp' in task data")

        with self.lock:
            self.priority_queues[priority].put((task_data["timestamp"], (task_id, task_data)))

    def get_next_task(self) -> Optional[tuple]:
        with self.lock:
            for priority in ["high", "medium", "low"]:
                if not self.priority_queues[priority].empty():
                    _, task = self.priority_queues[priority].get()
                    return task
        return None

    def queue_sizes(self) -> Dict[str, int]:
        return {level: self.priority_queues[level].qsize() for level in self.priority_queues}

    def is_empty(self) -> bool:
        return all(q.empty() for q in self.priority_queues.values())

    def clear_all(self):
        with self.lock:
            for q in self.priority_queues.values():
                while not q.empty():
                    q.get()

# Singleton instance
queue_manager = MultiAgentQueueManager()
