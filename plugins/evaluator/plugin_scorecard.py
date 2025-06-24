import time

class PluginScore:
    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id
        self.success_count = 0
        self.failure_count = 0
        self.total_runs = 0
        self.cpu_usage = []
        self.memory_usage = []
        self.exec_times = []
        self.last_updated = time.time()
        self.rating = 0.0

    def to_dict(self):
        return {
            "plugin_id": self.plugin_id,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "total_runs": self.total_runs,
            "cpu_avg": round(sum(self.cpu_usage) / len(self.cpu_usage), 2) if self.cpu_usage else 0.0,
            "memory_avg": round(sum(self.memory_usage) / len(self.memory_usage), 2) if self.memory_usage else 0.0,
            "exec_avg": round(sum(self.exec_times) / len(self.exec_times), 2) if self.exec_times else 0.0,
            "rating": round(self.rating, 2),
            "last_updated": self.last_updated
        }

    def update_stats(self, success: bool, cpu: float, memory: float, exec_time: float):
        self.total_runs += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        self.cpu_usage.append(cpu)
        self.memory_usage.append(memory)
        self.exec_times.append(exec_time)
        self.last_updated = time.time()
