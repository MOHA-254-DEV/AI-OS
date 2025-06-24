# /core/task_router_ai/history_db.py

import json
import os
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

DEFAULT_DB_PATH = "data/agent_task_history.json"

class AgentHistoryDB:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.db: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._load()

    def _load(self):
        """Load history from disk if available."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.db.update({k: v for k, v in data.items()})
            except Exception as e:
                print(f"[AgentHistoryDB] Failed to load history: {e}")

    def _save(self):
        """Persist current memory to disk."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, 'w') as f:
                json.dump(self.db, f, indent=2)
        except Exception as e:
            print(f"[AgentHistoryDB] Failed to save history: {e}")

    def record_task_result(self, agent_id: str, task_type: str, success: bool, duration: float):
        """Log a task outcome for an agent."""
        entry = {
            "task_type": task_type,
            "success": success,
            "duration": duration,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.db[agent_id].append(entry)
        self._save()

    def get_agent_history(self, agent_id: str) -> List[Dict[str, Any]]:
        return self.db.get(agent_id, [])

    def get_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.db

    def clear(self):
        """Clear all history (useful for tests)."""
        self.db.clear()
        self._save()
