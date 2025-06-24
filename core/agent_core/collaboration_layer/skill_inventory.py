import os
import json
import threading
import logging
from typing import List, Dict, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SkillInventory:
    def __init__(self, path: str = "agent_skills.json"):
        self.path = path
        self.lock = threading.Lock()
        if not os.path.exists(self.path):
            logging.info("Initializing skill inventory store.")
            self._init_store()

    def _init_store(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({}, f)
        except Exception as e:
            logging.error(f"Failed to initialize store: {e}")

    def _read_store(self) -> Dict:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to read skill store: {e}")
            return {}

    def _write_store(self, data: Dict):
        try:
            temp_path = f"{self.path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            os.replace(temp_path, self.path)
        except Exception as e:
            logging.error(f"Failed to write skill store: {e}")

    def load(self) -> Dict:
        with self.lock:
            return self._read_store()

    def save(self, data: Dict):
        with self.lock:
            self._write_store(data)

    def register_agent(self, agent_id: str, skillset: List[str]):
        if not agent_id or not isinstance(skillset, list):
            logging.warning("Invalid input for agent registration.")
            return
        skillset = [s.lower() for s in skillset]
        data = self.load()
        data[agent_id] = {
            "skills": skillset,
            "active": True,
            "role": "unassigned"
        }
        self.save(data)
        logging.info(f"Agent '{agent_id}' registered with skills: {skillset}")

    def update_skills(self, agent_id: str, new_skills: List[str]):
        if not isinstance(new_skills, list):
            logging.warning("Invalid skill set format.")
            return
        new_skills = [s.lower() for s in new_skills]
        data = self.load()
        if agent_id in data:
            data[agent_id]["skills"] = new_skills
            self.save(data)
            logging.info(f"Skills updated for agent '{agent_id}': {new_skills}")
        else:
            logging.warning(f"Agent '{agent_id}' not found.")

    def set_role(self, agent_id: str, role: str):
        data = self.load()
        if agent_id in data:
            data[agent_id]["role"] = role
            self.save(data)
            logging.info(f"Assigned role '{role}' to agent '{agent_id}'")
        else:
            logging.warning(f"Agent '{agent_id}' not found.")

    def deactivate_agent(self, agent_id: str):
        data = self.load()
        if agent_id in data:
            data[agent_id]["active"] = False
            self.save(data)
            logging.info(f"Agent '{agent_id}' deactivated.")
        else:
            logging.warning(f"Agent '{agent_id}' not found.")

    def activate_agent(self, agent_id: str):
        data = self.load()
        if agent_id in data:
            data[agent_id]["active"] = True
            self.save(data)
            logging.info(f"Agent '{agent_id}' activated.")
        else:
            logging.warning(f"Agent '{agent_id}' not found.")

    def get_agent_skills(self, agent_id: str) -> List[str]:
        return self.load().get(agent_id, {}).get("skills", [])

    def get_best_agents(self, required_skills: List[str], role: Optional[str] = None) -> List:
        if not isinstance(required_skills, list):
            logging.warning("Invalid skills input.")
            return []
        required_skills = set(s.lower() for s in required_skills)
        data = self.load()

        matches = {}
        for agent_id, info in data.items():
            if not info.get("active"):
                continue
            if role and info.get("role") != role:
                continue
            skill_overlap = len(set(info["skills"]) & required_skills)
            matches[agent_id] = skill_overlap

        sorted_matches = sorted(matches.items(), key=lambda item: item[1], reverse=True)
        return sorted_matches

# ✅ Example usage
if __name__ == "__main__":
    inv = SkillInventory()

    inv.register_agent("agent_1", ["Python", "Data Analysis", "ML"])
    inv.register_agent("agent_2", ["Cloud", "Java", "Kubernetes"])
    
    inv.update_skills("agent_1", ["Python", "Data Science", "Deep Learning"])
    inv.set_role("agent_1", "AI Developer")
    inv.set_role("agent_2", "DevOps Engineer")

    print("\nAgent 1 Skills:", inv.get_agent_skills("agent_1"))

    required = ["python", "deep learning"]
    top_agents = inv.get_best_agents(required)
    print(f"\nTop agents for {required}:", top_agents)
