from enum import Enum

class EventType(str, Enum):
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    TASK_FEEDBACK = "task_feedback"
    TASK_RETRY = "task_retry"
    AGENT_MESSAGE = "agent_message"
