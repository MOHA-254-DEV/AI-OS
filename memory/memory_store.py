# memory/memory_store.py

import json
import os
from collections import defaultdict
from datetime import datetime

class MemoryStore:
    def __init__(self, memory_dir="data/memory"):
        self.memory_dir = memory_dir
        self.short_term = defaultdict(list)  # {agent_name: [mem1, mem2]}
        self.long_term = defaultdict(list)
        os.makedirs(memory_dir, exist_ok=True)
        self._load_long_term()

    def _load_long_term(self):
        for file in os.listdir(self.memory_dir):
            path = os.path.join(self.memory_dir, file)
            if os.path.isfile(path) and file.endswith(".json"):
                agent = file.replace(".json", "")
                with open(path, "r") as f:
                    self.long_term[agent] = json.load(f)

    def add_memory(self, agent_name, memory, memory_type="short"):
        timestamped = {
            "timestamp": datetime.now().isoformat(),
            "memory": memory
        }

        if memory_type == "short":
            self.short_term[agent_name].append(timestamped)
        else:
            self.long_term[agent_name].append(timestamped)
            self._save_to_disk(agent_name)

    def _save_to_disk(self, agent_name):
        filepath = os.path.join(self.memory_dir, f"{agent_name}.json")
        with open(filepath, "w") as f:
            json.dump(self.long_term[agent_name], f, indent=2)

    def get_memory(self, agent_name, memory_type="short", limit=10):
        source = self.short_term if memory_type == "short" else self.long_term
        return source.get(agent_name, [])[-limit:]

    def search_memory(self, agent_name, keyword):
        all_memories = self.short_term.get(agent_name, []) + self.long_term.get(agent_name, [])
        return [m for m in all_memories if keyword.lower() in json.dumps(m).lower()]
