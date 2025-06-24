# system/agent/agent_status.py

from datetime import datetime

class AgentStatusTracker:
    def __init__(self):
        self.status = {}
        self.results = {}
        self.errors = {}

    def update_status(self, agent_id, status):
        print(f"[StatusTracker] {agent_id} -> {status}")
        self.status[agent_id] = {
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }

    def update_result(self, agent_id, result):
        self.results[agent_id] = result

    def log_error(self, agent_id, error):
        self.errors[agent_id] = {
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_status(self, agent_id):
        return self.status.get(agent_id, {}).get("status", "unknown")

    def get_all_active(self):
        return [aid for aid, stat in self.status.items() if stat["status"] in ["running", "queued"]]

    def get_result(self, agent_id):
        return self.results.get(agent_id)

    def get_error(self, agent_id):
        return self.errors.get(agent_id)
