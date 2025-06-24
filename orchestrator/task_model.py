from enum import Enum
import uuid
import time

class TaskStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

class AITask:
    def __init__(self, plugin, args, priority=5, max_retries=3):
        self.id = str(uuid.uuid4())
        self.plugin = plugin
        self.args = args
        self.priority = priority
        self.retries = 0
        self.max_retries = max_retries
        self.status = TaskStatus.QUEUED
        self.created_at = time.time()
        self.updated_at = time.time()

    def can_retry(self):
        return self.retries < self.max_retries
