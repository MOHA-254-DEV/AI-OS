# File: scheduler/context_scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from memory.temporal_sync import TemporalMemory
from tasks.task_engine import TaskEngine

class ContextScheduler:
    def __init__(self, agent_id):
        self.memory = TemporalMemory(agent_id)
        self.scheduler = BackgroundScheduler()
        self.task_engine = TaskEngine(agent_id)

    def start(self):
        self.scheduler.add_job(self.sync_daily_memory, 'interval', minutes=30)
        self.scheduler.add_job(self.sync_weekly_memory, 'interval', hours=6)
        self.scheduler.add_job(self.flush_memory, 'cron', hour=0)
        self.scheduler.start()

    def sync_daily_memory(self):
        print("[ContextScheduler] Syncing daily memory")
        context = {
            "agent_mood": "stable",
            "active_tasks": self.task_engine.get_active_tasks(),
            "summary": self.task_engine.get_recent_activity_summary()
        }
        self.memory.update_memory(context, memory_type="daily")

    def sync_weekly_memory(self):
        print("[ContextScheduler] Syncing weekly memory")
        context = {
            "performance_score": self.task_engine.get_performance_score(),
            "task_trends": self.task_engine.analyze_trends()
        }
        self.memory.update_memory(context, memory_type="weekly")

    def flush_memory(self):
        print("[ContextScheduler] Flushing old memory")
        self.memory.flush_old_memory()

    def shutdown(self):
        self.scheduler.shutdown()
