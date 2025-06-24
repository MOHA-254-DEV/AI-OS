import json
import os
import time

class UsageTracker:
    def __init__(self, usage_file='plugin_store/licensing/usage_log.json'):
        self.usage_file = usage_file
        self._load()

    def _load(self):
        if os.path.exists(self.usage_file):
            with open(self.usage_file, 'r') as f:
                self.usage = json.load(f)
        else:
            self.usage = {}

    def _save(self):
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2)

    def log_usage(self, user_email, plugin_id):
        key = f"{user_email}:{plugin_id}"
        if key not in self.usage:
            self.usage[key] = {"count": 0, "last_used": time.time()}
        self.usage[key]["count"] += 1
        self.usage[key]["last_used"] = time.time()
        self._save()

    def get_usage_count(self, user_email, plugin_id):
        key = f"{user_email}:{plugin_id}"
        return self.usage.get(key, {}).get("count", 0)

    def enforce_limit(self, user_email, plugin_id, max_uses=10):
        count = self.get_usage_count(user_email, plugin_id)
        return count <= max_uses
