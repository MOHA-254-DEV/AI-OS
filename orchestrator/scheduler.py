from profiler.profiler_core import ProfilerCore

class Scheduler:
    def __init__(self):
        self.profiler = ProfilerCore()

    def run_task(self, task):
        metrics = self.profiler.track_task(task.task_id, task.plugin["name"])
        try:
            result = self._execute_plugin(task)
            self.profiler.complete_task(task.task_id, status="success", result=result)
        except Exception as e:
            self.profiler.complete_task(task.task_id, status="failed", result=str(e))
