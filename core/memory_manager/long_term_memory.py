from .memory_interface import MemoryInterface
from .memory_config import load_config
import json, os
from typing import List

class LongTermMemory(MemoryInterface):
    def __init__(self):
        config = load_config()
        self.path = config.get("long_term_storage", "long_term_mem.json")
        os.makedirs(os.path.dirname(self.path), exist_ok=True) if os.path.dirname(self.path) else None
        if not os.path.exists(self.path):
            self._save({})
    
    def store(self, key: str, data: str) -> None:
        memory = self._load()
        memory[key] = data
        self._save(memory)

    def retrieve(self, key: str) -> str:
        memory = self._load()
        return memory.get(key, "")

    def search(self, query: str, top_k: int = 3) -> List[str]:
        memory = self._load()
        scored = [(v, v.lower().count(query.lower())) for v in memory.values() if query.lower() in v.lower()]
        sorted_matches = sorted(scored, key=lambda x: -x[1])
        return [match[0] for match in sorted_matches[:top_k]]

    def delete(self, key: str) -> None:
        memory = self._load()
        if key in memory:
            del memory[key]
            self._save(memory)

    def list_keys(self) -> List[str]:
        return list(self._load().keys())

    def _load(self) -> dict:
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save(self, memory: dict) -> None:
        try:
            with open(self.path, 'w') as f:
                json.dump(memory, f, indent=2)
        except Exception as e:
            print(f"[LongTermMemory] Failed to save memory: {e}")
