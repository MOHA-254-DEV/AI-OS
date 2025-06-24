import random
import time
from plugins.evaluator.rating_engine import PluginRatingEngine
from plugins.evaluator.blacklist import PluginBlacklist

class PluginMonitor:
    def __init__(self):
        self.rater = PluginRatingEngine()
        self.blacklist = PluginBlacklist()

    def record_execution(self, plugin_id: str, success: bool):
        cpu = random.uniform(1.0, 30.0)  # Simulated
        mem = random.uniform(10.0, 150.0)
        exec_time = random.uniform(0.2, 4.0)
        self.rater.update_plugin_score(plugin_id, success, cpu, mem, exec_time)
        score = self.rater.get_or_create_score(plugin_id)
        self.blacklist.check_and_blacklist(score)

    def get_scores(self):
        return self.rater.get_scorecard()

    def get_blacklisted(self):
        return self.blacklist.get_blacklisted()
