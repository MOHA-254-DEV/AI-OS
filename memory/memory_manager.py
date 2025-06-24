# memory/memory_manager.py

from memory.memory_store import MemoryStore

class MemoryManager:
    def __init__(self):
        self.store = MemoryStore()

    def record_task(self, agent_name, task_description, result):
        self.store.add_memory(agent_name, {
            "type": "task",
            "task": task_description,
            "result": result
        }, memory_type="short")

    def commit_to_long_term(self, agent_name):
        short_mem = self.store.get_memory(agent_name, "short")
        for m in short_mem:
            self.store.add_memory(agent_name, m["memory"], memory_type="long")
        self.store.short_term[agent_name] = []

    def retrieve_recent(self, agent_name, limit=5):
        return self.store.get_memory(agent_name, "short", limit)

    def find_by_keyword(self, agent_name, keyword):
        return self.store.search_memory(agent_name, keyword)
