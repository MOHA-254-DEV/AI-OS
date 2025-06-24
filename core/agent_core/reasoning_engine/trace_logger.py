import json
import os
from datetime import datetime
from typing import Any, Dict, List, Callable, Optional


class TraceLogger:
    """
    Enhanced logger for capturing agent chain-of-thought reasoning.
    Stores steps in memory and saves structured trace files for future analysis.
    """

    def __init__(
        self,
        agent_id: str,
        task_id: str,
        log_dir: str = "logs",
        redact_fields: Optional[List[str]] = None,
        auto_analyzer: Optional[Callable[[List[Dict[str, Any]]], Dict[str, Any]]] = None
    ):
        self.agent_id = agent_id
        self.task_id = task_id
        self.trace: List[Dict[str, Any]] = []
        self.timestamp = datetime.utcnow().isoformat()
        self.redact_fields = redact_fields or []
        self.auto_analyzer = auto_analyzer

        # Structured log directory (e.g., logs/2025-06-22/)
        today = datetime.utcnow().strftime("%Y-%m-%d")
        self.log_dir = os.path.join(log_dir, today)
        os.makedirs(self.log_dir, exist_ok=True)

    def log_step(self, step_name: str, details: Dict[str, Any]) -> None:
        """
        Add a reasoning step to the internal trace.
        """
        if not step_name or not isinstance(step_name, str):
            raise ValueError("Step name must be a non-empty string.")
        if not isinstance(details, dict):
            raise ValueError("Details must be a dictionary.")

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step": step_name,
            "details": self._redact(details)
        }
        self.trace.append(log_entry)

    def _redact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes sensitive fields from a dict.
        """
        return {k: ("[REDACTED]" if k in self.redact_fields else v) for k, v in data.items()}

    def preview_trace(self, last_n: int = 3) -> List[Dict[str, Any]]:
        """
        Preview the last N steps.
        """
        return self.trace[-last_n:]

    def save(self) -> str:
        """
        Save the full trace log to a structured JSON file.
        Auto-analyzes if configured.
        """
        filename = f"{self.agent_id}_{self.task_id}_{datetime.utcnow().strftime('%H%M%S')}.json"
        filepath = os.path.join(self.log_dir, filename)

        trace_data = {
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "timestamp": self.timestamp,
            "trace": self.trace,
        }

        # Optionally append meta-analysis
        if self.auto_analyzer:
            try:
                analysis = self.auto_analyzer(self.trace)
                trace_data["meta_analysis"] = analysis
            except Exception as e:
                trace_data["meta_analysis_error"] = str(e)

        with open(filepath, 'w') as f:
            json.dump(trace_data, f, indent=4)

        print(f"[TraceLogger] ✅ Trace saved at: {filepath}")
        return filepath
