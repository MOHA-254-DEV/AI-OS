import time
from collections import defaultdict

class AgentTracker:
    def __init__(self):
        self.agent_activity = defaultdict(list)  # agent_id -> [activity dicts]

    def log_activity(self, agent_id: str, task_type: str, plugin: str, outcome: str):
        entry = {
            "timestamp": time.time(),
            "task_type": task_type,
            "plugin": plugin,
            "outcome": outcome,
        }
        self.agent_activity[agent_id].append(entry)

    def get_agent_logs(self, agent_id: str, limit=100):
        return self.agent_activity[agent_id][-limit:]

    def get_all_logs(self, limit=500):
        all_logs = []
        for agent, logs in self.agent_activity.items():
            all_logs.extend(logs[-limit:])
        return sorted(all_logs, key=lambda x: x['timestamp'], reverse=True)[:limit]
