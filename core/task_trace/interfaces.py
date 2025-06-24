from datetime import datetime
from typing import Dict, Any


class Trace:
    def __init__(
        self,
        trace_id: str,
        agent_id: str,
        task: str,
        action: str,
        result: str,
        timestamp: str = None,
        metadata: Dict[str, Any] = None,
        level: str = "INFO",
        action_type: str = "operation"
    ):
        self.trace_id = trace_id
        self.agent_id = agent_id
        self.task = task
        self.action = action
        self.result = result
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.metadata = metadata or {}
        self.level = level
        self.action_type = action_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "agent_id": self.agent_id,
            "task": self.task,
            "action": self.action,
            "result": self.result,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "level": self.level,
            "action_type": self.action_type
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trace':
        return cls(
            trace_id=data["trace_id"],
            agent_id=data["agent_id"],
            task=data["task"],
            action=data["action"],
            result=data["result"],
            timestamp=data.get("timestamp"),
            metadata=data.get("metadata", {}),
            level=data.get("level", "INFO"),
            action_type=data.get("action_type", "operation")
        )

    def __repr__(self):
        return f"<Trace {self.trace_id} | {self.agent_id} | {self.task} | {self.result}>"
