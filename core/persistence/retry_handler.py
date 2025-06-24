# File: core/persistence/retry_handler.py

import time
from typing import Callable
from core.persistence.persistence_config import CONFIG

class RetryHandler:
    def __init__(self):
        self.failures = {}
        self.max_retries = CONFIG["max_retries"]
        self.retry_backoff = CONFIG["retry_backoff"]

    def track_failure(self, task_id: str) -> None:
        if task_id not in self.failures:
            self.failures[task_id] = 0
        self.failures[task_id] += 1

    def can_retry(self, task_id: str) -> bool:
        return self.failures.get(task_id, 0) < self.max_retries

    def get_backoff(self, task_id: str) -> int:
        retry_count = self.failures.get(task_id, 0)
        if retry_count < len(self.retry_backoff):
            return self.retry_backoff[retry_count]
        return self.retry_backoff[-1]

    def retry(self, task_id: str, func: Callable, *args, **kwargs):
        """
        Attempt a function call with retry and exponential backoff.
        """
        if not self.can_retry(task_id):
            print(f"[RetryHandler] Max retries reached for task '{task_id}'. Aborting.")
            return None

        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.track_failure(task_id)
            wait = self.get_backoff(task_id)
            print(f"[RetryHandler] Retry {self.failures[task_id]} for '{task_id}'. Waiting {wait}s due to error: {e}")
            time.sleep(wait)
            return self.retry(task_id, func, *args, **kwargs)
