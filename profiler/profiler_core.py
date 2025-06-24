import threading
import time
from profiler.task_metrics import TaskMetrics

class ProfilerCore:
    def __init__(self):
        self.active_tasks = {}
        self.task_results = []

    def track_task(self, task_id, plugin_name):
        metrics = TaskMetrics(task_id, plugin_name)
        metrics.begin()
        self.active_tasks[task_id] = metrics
        threading.Thread(target=self._monitor_usage, args=(metrics,), daemon=True).start()
        return metrics

    def _monitor_usage(self, metrics):
        while metrics.status == "pending":
            metrics.log_usage()
            time.sleep(0.2)

    def complete_task(self, task_id, status="success", result=None):
        if task_id in self.active_tasks:
            metrics = self.active_tasks[task_id]
            metrics.end(status, result)
            self.task_results.append(metrics.get_summary())
            del self.active_tasks[task_id]

    def get_all_results(self):
        return self.task_results

    def clear_results(self):
        self.task_results.clear()
