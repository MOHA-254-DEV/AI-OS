from enum import Enum
from typing import Optional
import uuid
import time

class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class Job:
    def __init__(self, task_type: str, payload: dict, priority: int = 5, retries: int = 0):
        self.id = str(uuid.uuid4())
        self.task_type = task_type
        self.payload = payload
        self.priority = priority
        self.status = JobStatus.QUEUED
        self.created_at = time.time()
        self.updated_at = self.created_at
        self.result = None
        self.retries = retries
        self.logs = []

    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "payload": self.payload,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "result": self.result,
            "retries": self.retries,
            "logs": self.logs
        }
