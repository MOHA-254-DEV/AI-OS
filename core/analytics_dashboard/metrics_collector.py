from collections import defaultdict
from datetime import datetime
import threading
from typing import Dict, List, Union


class MetricsCollector:
    """
    In-memory thread-safe collector for agent task and error metrics.
    """

    def __init__(self):
        self.metrics: Dict[str, List[Dict[str, Union[str, datetime]]]] = defaultdict(list)
        self.lock = threading.Lock()

    def record_task(self, agent_id: str, task_type: str, status: str) -> None:
        """
        Logs a completed task for analytics purposes.

        Args:
            agent_id (str): Unique agent identifier.
            task_type (str): Type of the task (e.g., 'design', 'seo').
            status (str): Task result status ('success', 'failure', etc.).
        """
        try:
            with self.lock:
                self.metrics["tasks"].append({
                    "agent_id": agent_id,
                    "task_type": task_type,
                    "status": status,
                    "timestamp": datetime.utcnow().isoformat()
                })
        except Exception as e:
            print(f"[MetricsCollector] Failed to record task: {e}")

    def record_error(self, agent_id: str, error_message: str) -> None:
        """
        Logs an error event from an agent.

        Args:
            agent_id (str): Agent that experienced the error.
            error_message (str): Description of the error.
        """
        try:
            with self.lock:
                self.metrics["errors"].append({
                    "agent_id": agent_id,
                    "error": error_message,
                    "timestamp": datetime.utcnow().isoformat()
                })
        except Exception as e:
            print(f"[MetricsCollector] Failed to record error: {e}")

    def get_metrics(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Retrieves all recorded metrics.

        Returns:
            Dict[str, List[Dict[str, str]]]: Dictionary with 'tasks' and 'errors'.
        """
        with self.lock:
            # Ensure both keys exist
            return {
                "tasks": list(self.metrics.get("tasks", [])),
                "errors": list(self.metrics.get("errors", []))
            }

    def reset_metrics(self) -> None:
        """
        Clears all collected metrics (useful between report intervals).
        """
        with self.lock:
            self.metrics.clear()
