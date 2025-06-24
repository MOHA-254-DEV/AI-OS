# scheduler/task_queue.py

import heapq
from time import time
from threading import Lock
from priority_levels import Priority

class TaskQueue:
    def __init__(self):
        self.queue = []
        self.lock = Lock()

    def add_task(self, task, priority=Priority.MEDIUM):
        with self.lock:
            heapq.heappush(self.queue, (-priority, time(), task))

    def get_next_task(self):
        with self.lock:
            if self.queue:
                _, _, task = heapq.heappop(self.queue)
                return task
            return None

    def has_tasks(self):
        return len(self.queue) > 0
