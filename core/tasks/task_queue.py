# File: core/tasks/task_queue.py

import heapq
import itertools
from typing import Any, List, Tuple

class TaskQueue:
    def __init__(self):
        self.queue: List[Tuple[int, int, Any]] = []
        self.counter = itertools.count()  # ensures stable ordering

    def add_task(self, task: Any, priority: int = 1):
        count = next(self.counter)
        heapq.heappush(self.queue, (priority, count, task))

    def get_next_task(self) -> Any:
        if self.queue:
            return heapq.heappop(self.queue)[2]
        return None

    def peek(self) -> Any:
        if self.queue:
            return self.queue[0][2]
        return None

    def has_tasks(self) -> bool:
        return bool(self.queue)

    def __len__(self) -> int:
        return len(self.queue)

    def __repr__(self) -> str:
        return f"<TaskQueue size={len(self.queue)} next={self.peek()}>"
