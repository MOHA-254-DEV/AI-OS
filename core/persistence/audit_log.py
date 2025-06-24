# File: core/persistence/audit_log.py

import os
import json
from datetime import datetime
from typing import Dict, List
from threading import Lock

AUDIT_LOG = "./logs/recovery_audit.json"
os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)

class AuditLog:
    _lock = Lock()

    def __init__(self, path: str = AUDIT_LOG):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump([], f, indent=2)

    def log(self, agent_id: str, action: str, meta: Dict, flush: bool = False) -> None:
        """
        Append an audit log entry.

        Args:
            agent_id: The identifier of the affected agent.
            action: The action performed (e.g., restart, reroute).
            meta: Extra metadata.
            flush: If True, appends without reading previous logs.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "action": action,
            "meta": meta
        }

        try:
            with self._lock:
                if flush:
                    # Append without loading entire file (faster, less safe if format is corrupt)
                    logs = self._safe_read()
                    logs.append(entry)
                else:
                    logs = self._safe_read()
                    logs.append(entry)

                self._safe_write(logs)

        except Exception as e:
            print(f"[AuditLog] Failed to write audit entry: {e}")

    def _safe_read(self) -> List[Dict]:
        """
        Safely read the existing audit log. Returns empty list on error.
        """
        if not os.path.exists(self.path):
            return []

        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _safe_write(self, logs: List[Dict]) -> None:
        """
        Safely write audit log list to file.
        """
        with open(self.path, 'w') as f:
            json.dump(logs, f, indent=2)
