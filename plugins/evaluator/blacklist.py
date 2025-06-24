class PluginBlacklist:
    def __init__(self):
        self.blacklisted = set()

    def check_and_blacklist(self, score_obj):
        if score_obj.rating < 10 and score_obj.total_runs > 5:
            self.blacklisted.add(score_obj.plugin_id)

    def is_blacklisted(self, plugin_id: str) -> bool:
        return plugin_id in self.blacklisted

    def get_blacklisted(self):
        return list(self.blacklisted)
