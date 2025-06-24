# task_scheduler.py - placeholder
# scheduler/task_scheduler.py

import threading
import time

class TaskScheduler:
    def __init__(self, task_queue, task_delegator, interval=3):
        self.task_queue = task_queue
        self.delegator = task_delegator
        self.interval = interval
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.start()

    def _run_loop(self):
        while self.running:
            if self.task_queue.has_tasks():
                task = self.task_queue.get_next_task()
                result = self.delegator.delegate(task)
                print(f"[Scheduler] Executed task: {task['data']} ➜ {result}")
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
