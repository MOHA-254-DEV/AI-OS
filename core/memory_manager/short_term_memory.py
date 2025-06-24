import time
from typing import Dict, List
from .memory_interface import MemoryInterface
from .memory_config import load_config


class ShortTermMemory(MemoryInterface):
    def __init__(self):
        self.memory: Dict[str, Dict[str, any]] = {}
        config = load_config()
        self.ttl = config.get("short_term_ttl", 3600)  # Default TTL: 1 hour

    def store(self, key: str, data: str) -> None:
        self.memory[key] = {
            "data": data,
            "timestamp": time.time()
        }

    def retrieve(self, key: str) -> str:
        self._cleanup_expired()
        entry = self.memory.get(key)
        return entry["data"] if entry else ""

    def search(self, query: str, top_k: int = 3) -> List[str]:
        self._cleanup_expired()
        matches = [
            entry["data"]
            for entry in self.memory.values()
            if query.lower() in entry["data"].lower()
        ]
        return sorted(matches, key=lambda x: -x.lower().count(query.lower()))[:top_k]

    def delete(self, key: str) -> None:
        self.memory.pop(key, None)

    def list_keys(self) -> List[str]:
        self._cleanup_expired()
        return list(self.memory.keys())

    def _cleanup_expired(self) -> None:
        now = time.time()
        expired_keys = [key for key, entry in self.memory.items() if now - entry["timestamp"] > self.ttl]
        for key in expired_keys:
            del self.memory[key]
