import uuid
import time
from datetime import datetime
from .trace_storage import TraceStorage

class ExecutionLogger:
    def __init__(self):
        self.storage = TraceStorage()

    def log(self, agent_id, task_name, action, result, metadata=None, level="INFO", action_type="operation"):
        trace_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        trace_record = {
            "trace_id": trace_id,
            "timestamp": timestamp,
            "agent_id": agent_id,
            "task": task_name,
            "action": action,
            "result": result,
            "level": level,
            "action_type": action_type,
            "metadata": metadata or {}
        }

        self.storage.store_trace(trace_record)
        return trace_id

    def time_action(self, agent_id, task_name, action_label, func, *args, **kwargs):
        """
        Automatically logs the start/end time, duration, and result of a function.
        """
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = round(time.time() - start, 4)
            self.log(
                agent_id=agent_id,
                task_name=task_name,
                action=action_label,
                result="success",
                metadata={"duration_sec": duration},
                level="INFO"
            )
            return result
        except Exception as e:
            duration = round(time.time() - start, 4)
            self.log(
                agent_id=agent_id,
                task_name=task_name,
                action=action_label,
                result="failure",
                metadata={"duration_sec": duration, "error": str(e)},
                level="ERROR"
            )
            raise
