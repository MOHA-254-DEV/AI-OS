import json
import os
import threading
import logging
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GroupMemory:
    def __init__(self, path: str = "group_memory.json"):
        self.path = path
        self.lock = threading.Lock()
        if not os.path.exists(self.path):
            logging.info("[GroupMemory] Initializing new memory store.")
            self._init_memory()

    def _init_memory(self):
        default_memory = {
            "agents": {},
            "tasks": [],
            "results": {}
        }
        self._write_memory(default_memory)

    def _read_memory(self) -> Dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_memory(self, memory: Dict[str, Any]):
        temp_path = f"{self.path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=4)
        os.replace(temp_path, self.path)

    def load(self) -> Dict[str, Any]:
        with self.lock:
            return self._read_memory()

    def save(self, memory: Dict[str, Any]):
        with self.lock:
            self._write_memory(memory)

    def update_agent_context(self, agent_id: str, context: Dict[str, Any]):
        with self.lock:
            memory = self.load()
            memory["agents"][agent_id] = context
            self.save(memory)
            logging.info(f"[GroupMemory] Updated context for agent: {agent_id}")

    def log_task(self, task_info: Dict[str, Any]):
        with self.lock:
            memory = self.load()
            if not isinstance(task_info, dict) or "task_id" not in task_info:
                raise ValueError("Invalid task_info format. Must include 'task_id'.")
            memory["tasks"].append(task_info)
            self.save(memory)
            logging.info(f"[GroupMemory] Logged task: {task_info.get('task_id')}")

    def add_result(self, task_id: str, result: Dict[str, Any]):
        with self.lock:
            memory = self.load()
            memory["results"][task_id] = result
            self.save(memory)
            logging.info(f"[GroupMemory] Added result for task: {task_id}")

    def remove_agent(self, agent_id: str):
        with self.lock:
            memory = self.load()
            if agent_id in memory["agents"]:
                del memory["agents"][agent_id]
                self.save(memory)
                logging.info(f"[GroupMemory] Removed agent: {agent_id}")
            else:
                logging.warning(f"[GroupMemory] Agent {agent_id} not found.")

    def get_task_results(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            memory = self.load()
            result = memory["results"].get(task_id)
            if result:
                logging.info(f"[GroupMemory] Retrieved result for task: {task_id}")
            else:
                logging.warning(f"[GroupMemory] No result found for task: {task_id}")
            return result

    def get_all_agents(self) -> Dict[str, Any]:
        with self.lock:
            return self.load()["agents"]

    def get_all_tasks(self) -> list:
        with self.lock:
            return self.load()["tasks"]

    def get_all_results(self) -> Dict[str, Any]:
        with self.lock:
            return self.load()["results"]

# ✅ Test mode
if __name__ == "__main__":
    gm = GroupMemory()

    gm.update_agent_context("agent_planner_1", {"name": "Planner A", "role": "planner"})
    gm.log_task({"task_id": "task_001", "description": "Analyze project scope."})
    gm.add_result("task_001", {"status": "done", "output": "Project scope analyzed."})
    
    print("Task Result:", gm.get_task_results("task_001"))
    print("All Agents:", gm.get_all_agents())
