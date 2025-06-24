import os
import json
import threading

class EventStore:
    def __init__(self, log_path="logs/event_log.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.lock = threading.Lock()

    def save_event(self, event_data: str):
        try:
            with self.lock, open(self.log_path, 'a') as f:
                f.write(event_data + "\n")
        except Exception as e:
            print(f"[EventStore] Failed to save event: {e}")

    def get_all(self):
        try:
            with open(self.log_path, 'r') as f:
                return [json.loads(line.strip()) for line in f if line.strip()]
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"[EventStore] Failed to load events: {e}")
            return []

    def get_events_by_agent(self, agent_id):
        return [e for e in self.get_all() if e.get("agent_id") == agent_id]
