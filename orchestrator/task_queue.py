import heapq
import threading

class TaskQueue:
    def __init__(self):
        self.lock = threading.Lock()
        self.tasks = []

    def enqueue(self, task):
        with self.lock:
            heapq.heappush(self.tasks, (-task.priority, task))

    def dequeue(self):
        with self.lock:
            if self.tasks:
                return heapq.heappop(self.tasks)[1]
            return None

    def is_empty(self):
        with self.lock:
            return len(self.tasks) == 0

    def size(self):
        with self.lock:
            return len(self.tasks)
