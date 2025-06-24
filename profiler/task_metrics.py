import time
import psutil
import uuid

class TaskMetrics:
    def __init__(self, task_id, plugin_name):
        self.task_id = task_id or str(uuid.uuid4())
        self.plugin_name = plugin_name
        self.start_time = None
        self.end_time = None
        self.cpu_usage = []
        self.mem_usage = []
        self.status = "pending"
        self.result = None

    def begin(self):
        self.start_time = time.time()

    def end(self, status="success", result=None):
        self.end_time = time.time()
        self.status = status
        self.result = result

    def log_usage(self):
        process = psutil.Process()
        self.cpu_usage.append(process.cpu_percent(interval=0.1))
        self.mem_usage.append(process.memory_info().rss)

    def get_summary(self):
        return {
            "task_id": self.task_id,
            "plugin": self.plugin_name,
            "runtime": round(self.end_time - self.start_time, 4) if self.end_time else None,
            "cpu_avg": round(sum(self.cpu_usage) / len(self.cpu_usage), 2) if self.cpu_usage else None,
            "mem_avg": round(sum(self.mem_usage) / len(self.mem_usage) / 1024 / 1024, 2) if self.mem_usage else None,
            "status": self.status
        }
