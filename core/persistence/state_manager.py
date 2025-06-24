# File: /core/persistence/state_manager.py

import os
import json
import time
from typing import Any, Dict

STATE_DIR = os.environ.get("AGENT_STATE_DIR", "./data/agent_state")


class StateManager:
    def __init__(self, agent_id: str):
        """
        Manages state persistence for a specific agent.
        Each agent gets its own JSON file for state storage.
        """
        self.agent_id = agent_id
        self.state_path = os.path.join(STATE_DIR, f"{agent_id}.json")
        os.makedirs(STATE_DIR, exist_ok=True)

    def save_state(self, state: Dict[str, Any]) -> bool:
        """
        Saves the state of the agent to disk with a timestamp.
        Returns True if successful.
        """
        state["_last_saved"] = time.time()
        try:
            with open(self.state_path, "w") as f:
                json.dump(state, f, indent=2)
            return True
        except Exception as e:
            print(f"[StateManager] Failed to save state: {e}")
            return False

    def load_state(self) -> Dict[str, Any]:
        """
        Loads the agent's state from disk. Returns empty dict if not found or error.
        """
        if not os.path.exists(self.state_path):
            return {}
        try:
            with open(self.state_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[StateManager] Failed to load state: {e}")
            return {}

    def delete_state(self) -> bool:
        """
        Deletes the agent's saved state file.
        Returns True if the file was deleted.
        """
        if os.path.exists(self.state_path):
            try:
                os.remove(self.state_path)
                return True
            except Exception as e:
                print(f"[StateManager] Failed to delete state: {e}")
                return False
        return False

    def has_state(self) -> bool:
        """
        Checks if a state file exists for this agent.
        """
        return os.path.exists(self.state_path)
