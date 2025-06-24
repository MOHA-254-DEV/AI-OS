from collections import defaultdict, Counter

class BehaviorCache:
    def __init__(self):
        self.category_counter = Counter()
        self.plugin_counter = Counter()
        self.outcome_counter = Counter()
        self.timestamp_buckets = defaultdict(int)

    def update_from_log(self, logs):
        for log in logs:
            self.category_counter[log["task_type"]] += 1
            self.plugin_counter[log["plugin"]] += 1
            self.outcome_counter[log["outcome"]] += 1
            bucket = int(log["timestamp"]) // 60  # 1-minute buckets
            self.timestamp_buckets[bucket] += 1

    def get_snapshot(self):
        return {
            "categories": dict(self.category_counter),
            "plugins": dict(self.plugin_counter),
            "outcomes": dict(self.outcome_counter),
            "time_heat": dict(self.timestamp_buckets)
        }
