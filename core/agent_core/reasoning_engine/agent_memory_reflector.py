import logging
import os
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List

# Logging configuration
logging.basicConfig(
    filename='agent_memory.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EnhancedMemoryStore:
    """
    A memory store that supports TTL, persistence, and querying.
    """
    def __init__(self, ttl_seconds: int = 3600, persist_path: Optional[str] = None):
        self.ttl = timedelta(seconds=ttl_seconds)
        self.persist_path = persist_path
        self.store_data: Dict[str, Dict[str, Any]] = {}
        if persist_path:
            self._load()

    def _load(self):
        """Load persisted data from disk."""
        if os.path.exists(self.persist_path):
            with open(self.persist_path, 'r') as f:
                self.store_data = json.load(f)
            logging.info("Memory loaded from disk.")

    def _persist(self):
        """Persist memory to disk."""
        if self.persist_path:
            with open(self.persist_path, 'w') as f:
                json.dump(self.store_data, f, indent=2)
            logging.info("Memory persisted to disk.")

    def _is_expired(self, timestamp: str) -> bool:
        dt = datetime.fromisoformat(timestamp)
        return datetime.utcnow() - dt > self.ttl

    def store(self, agent_id: str, key: str, value: Any) -> None:
        if not agent_id or not isinstance(agent_id, str):
            raise ValueError("Invalid agent_id provided.")
        if not key or not isinstance(key, str):
            raise ValueError("Invalid memory key.")

        now = datetime.utcnow().isoformat()
        self.store_data.setdefault(agent_id, {})[key] = {
            "value": value,
            "timestamp": now
        }

        logging.info(f"Stored memory for agent='{agent_id}', key='{key}'")
        self._persist()

    def retrieve(self, agent_id: str, key: str) -> Optional[Dict[str, Any]]:
        agent_mem = self.store_data.get(agent_id, {})
        record = agent_mem.get(key)

        if not record:
            return None

        if self._is_expired(record["timestamp"]):
            logging.info(f"Memory expired for agent='{agent_id}', key='{key}'")
            return None

        logging.info(f"Retrieved memory for agent='{agent_id}', key='{key}'")
        return record

    def list_keys(self, agent_id: str, prefix: str = "", contains: str = "") -> List[str]:
        keys = list(self.store_data.get(agent_id, {}).keys())
        if prefix:
            keys = [k for k in keys if k.startswith(prefix)]
        if contains:
            keys = [k for k in keys if contains in k]
        return keys

    def clear_agent_memory(self, agent_id: str) -> None:
        if agent_id in self.store_data:
            del self.store_data[agent_id]
            logging.info(f"Cleared memory for agent='{agent_id}'")
            self._persist()


class EnhancedAgentMemoryReflector:
    """
    Reflects agent task outputs into memory for future access.
    """
    def __init__(self, memory_store: EnhancedMemoryStore):
        self.memory = memory_store

    def reflect(self, agent_id: str, task_id: str, summary_obj: Any) -> None:
        if not agent_id or not isinstance(agent_id, str):
            raise ValueError("Invalid agent_id.")
        if not task_id or not isinstance(task_id, str):
            raise ValueError("Invalid task_id.")
        if summary_obj is None:
            raise ValueError("Summary object cannot be None.")

        key = f"reflection::{task_id}"
        self.memory.store(agent_id, key, summary_obj)
        logging.info(f"Reflected summary for agent='{agent_id}', task='{task_id}'")

    def recall(self, agent_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        key = f"reflection::{task_id}"
        return self.memory.retrieve(agent_id, key)

    def list_reflections(self, agent_id: str) -> List[str]:
        return self.memory.list_keys(agent_id, prefix="reflection::")


# ======================
# ✅ Example usage stub:
# ======================
if __name__ == "__main__":
    # Configurable persistent memory with TTL (1 hour)
    store = EnhancedMemoryStore(ttl_seconds=3600, persist_path="agent_memory.json")
    reflector = EnhancedAgentMemoryReflector(store)

    # Sample data
    agent_id = "agent_007"
    task_id = "upload_summary"
    summary = {
        "status": "success",
        "file": "final_report.pdf",
        "description": "Successfully uploaded to S3 storage."
    }

    # Reflect + Retrieve
    reflector.reflect(agent_id, task_id, summary)

    recalled = reflector.recall(agent_id, task_id)
    print("\n📦 Retrieved memory:", recalled)

    # Query reflection keys
    keys = reflector.list_reflections(agent_id)
    print("🗂️  Reflection keys:", keys)
