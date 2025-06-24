import time
from collections import defaultdict

class PluginFeedbackTracker:
    def __init__(self):
        self.feedback_data = defaultdict(list)

    def add_feedback(self, plugin_name: str, agent_id: str, task_type: str, outcome: str, feedback_text: str = ""):
        entry = {
            "timestamp": time.time(),
            "plugin": plugin_name,
            "agent": agent_id,
            "task_type": task_type,
            "outcome": outcome,
            "feedback": feedback_text
        }
        self.feedback_data[plugin_name].append(entry)

    def get_feedback(self, plugin_name: str, limit: int = 50):
        return self.feedback_data[plugin_name][-limit:]

    def get_all_feedback(self):
        return self.feedback_data
