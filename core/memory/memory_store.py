from threading import Lock
from typing import Dict, List, Optional, Any


class MemoryStore:
    """
    In-memory memory store for agent memories with thread-safe access and retrieval utilities.
    """

    def __init__(self):
        self.memory_db: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()

    def insert(self, memory_object: Dict[str, Any]) -> None:
        """
        Inserts a memory object into the store.

        Args:
            memory_object (dict): The memory to store. Must contain 'id' and 'agent_id'.
        """
        if "id" not in memory_object or "agent_id" not in memory_object:
            raise ValueError("Memory object must contain 'id' and 'agent_id'.")

        with self.lock:
            self.memory_db[memory_object["id"]] = memory_object

    def get_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a memory by its unique ID.

        Args:
            memory_id (str): The memory ID to look up.

        Returns:
            dict or None: The memory object, or None if not found.
        """
        with self.lock:
            return self.memory_db.get(memory_id)

    def delete(self, memory_id: str) -> bool:
        """
        Deletes a memory from the store.

        Args:
            memory_id (str): The memory ID to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        with self.lock:
            if memory_id in self.memory_db:
                del self.memory_db[memory_id]
                return True
            return False

    def get_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all memories associated with a specific agent.

        Args:
            agent_id (str): The agent ID.

        Returns:
            List[Dict]: List of memory objects.
        """
        with self.lock:
            return [mem for mem in self.memory_db.values() if mem.get("agent_id") == agent_id]

    def list_all(self) -> List[Dict[str, Any]]:
        """
        Returns all memory entries.

        Returns:
            List[Dict]: All memory entries.
        """
        with self.lock:
            return list(self.memory_db.values())

    def filter_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Retrieves all memories with a specific tag.

        Args:
            tag (str): Tag to filter by.

        Returns:
            List[Dict]: Matching memory entries.
        """
        with self.lock:
            return [mem for mem in self.memory_db.values() if tag in mem.get("tags", [])]

    def count(self) -> int:
        """
        Returns the total number of memories.

        Returns:
            int: Memory count.
        """
        with self.lock:
            return len(self.memory_db)
