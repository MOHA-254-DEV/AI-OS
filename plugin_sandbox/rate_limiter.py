# plugin_sandbox/rate_limiter.py

import time
from collections import defaultdict

class PluginRateLimiter:
    def __init__(self, limit=5, window_sec=60):
        self.limit = limit
        self.window_sec = window_sec
        self.usage = defaultdict(list)

    def allow(self, plugin_name: str):
        now = time.time()
        self.usage[plugin_name] = [t for t in self.usage[plugin_name] if now - t < self.window_sec]
        if len(self.usage[plugin_name]) < self.limit:
            self.usage[plugin_name].append(now)
            return True
        return False

    def get_usage(self, plugin_name):
        return len(self.usage[plugin_name])
