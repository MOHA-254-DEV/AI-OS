import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from .memory_store import MemoryStore
from .semantic_search import SemanticSearchEngine

class MemoryEngine:
    def __init__(self):
        self.memory_store = MemoryStore()
        self.semantic_search = SemanticSearchEngine()

    def store_memory(
        self,
        content: str,
        tags: List[str],
        agent_id: str,
        importance: float = 0.5
    ) -> str:
        """
        Stores a memory and indexes it for semantic retrieval.

        Args:
            content (str): The text content of the memory.
            tags (List[str]): Related tags or labels.
            agent_id (str): The owning agent's identifier.
            importance (float): Importance score (0.0 - 1.0).

        Returns:
            str: The unique memory ID.
        """
        if not content or not agent_id:
            raise ValueError("Memory content and agent_id are required.")

        memory_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        memory_object = {
            "id": memory_id,
            "timestamp": timestamp,
            "content": content,
            "tags": tags,
            "agent_id": agent_id,
            "importance": importance
        }

        self.memory_store.insert(memory_object)

        try:
            self.semantic_search.index_memory(memory_id, content)
        except Exception as e:
            print(f"[Warning] Semantic index failed for {memory_id}: {e}")

        return memory_id

    def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a memory object by its ID.
        """
        return self.memory_store.get_by_id(memory_id)

    def delete_memory(self, memory_id: str) -> bool:
        """
        Deletes memory from both store and semantic index.
        """
        self.memory_store.delete(memory_id)
        try:
            self.semantic_search.remove_from_index(memory_id)
        except Exception as e:
            print(f"[Warning] Failed to remove memory from semantic index: {e}")
        return True

    def search_memories(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches memories using semantic similarity.

        Args:
            query (str): The semantic query.
            top_k (int): Max number of results to return.

        Returns:
            List[Dict]: Matched memory objects.
        """
        memory_ids = self.semantic_search.search(query, top_k=top_k)
        return [self.memory_store.get_by_id(mem_id) for mem_id in memory_ids if mem_id]

    def get_memories_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all memories associated with a given agent.
        """
        return self.memory_store.get_by_agent(agent_id)

    def summarize_agent_memory(self, agent_id: str, max_chars: int = 500) -> str:
        """
        Creates a naive summary of an agent's memory.

        Args:
            agent_id (str): The agent ID.
            max_chars (int): Character limit for summary.

        Returns:
            str: Concatenated memory content summary.
        """
        memories = self.get_memories_by_agent(agent_id)
        sorted_memories = sorted(memories, key=lambda m: m.get("importance", 0), reverse=True)

        summary = " ".join(mem["content"] for mem in sorted_memories)
        return f"Summary for Agent {agent_id}: {summary[:max_chars]}..."

    def prune_low_importance(self, agent_id: str, threshold: float = 0.2) -> int:
        """
        Removes memories below a certain importance threshold.

        Args:
            agent_id (str): Agent whose memories to check.
            threshold (float): Importance cutoff.

        Returns:
            int: Number of pruned memories.
        """
        memories = self.get_memories_by_agent(agent_id)
        to_delete = [m["id"] for m in memories if m.get("importance", 0) < threshold]

        for mem_id in to_delete:
            self.delete_memory(mem_id)

        return len(to_delete)
