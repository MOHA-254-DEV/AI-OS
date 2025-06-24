# File: core/memory_manager/memory_engine.py

from .short_term_memory import ShortTermMemory
from .long_term_memory import LongTermMemory
from typing import Dict, List

class MemoryEngine:
    """
    Unified interface for short-term and long-term memory operations.
    """
    def __init__(self):
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()

    def remember(self, key: str, data: str, persistent: bool = False) -> None:
        """
        Store data in memory. Short-term by default, long-term if persistent=True.
        """
        self.stm.store(key, data)
        if persistent:
            self.ltm.store(key, data)

    def recall(self, key: str) -> str:
        """
        Try to retrieve memory from short-term first, fallback to long-term.
        """
        data = self.stm.retrieve(key)
        return data if data else self.ltm.retrieve(key)

    def forget(self, key: str) -> None:
        """
        Remove the memory from both short and long-term.
        """
        self.stm.delete(key)
        self.ltm.delete(key)

    def context_search(self, query: str, top_k: int = 3) -> List[str]:
        """
        Search memory content using keyword match in both stores.
        """
        results_stm = self.stm.search(query, top_k)
        results_ltm = self.ltm.search(query, top_k)
        return list(set(results_stm + results_ltm))

    def list_memory(self) -> Dict[str, List[str]]:
        """
        Return all keys in both memory stores.
        """
        return {
            "short_term": self.stm.list_keys(),
            "long_term": self.ltm.list_keys()
        }
