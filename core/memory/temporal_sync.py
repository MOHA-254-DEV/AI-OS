# File: memory/temporal_sync.py

import json
import os
from datetime import datetime, timedelta
import threading
from utils.encryption import encrypt_data, decrypt_data

MEMORY_DIR = "memory_store/temporal/"
os.makedirs(MEMORY_DIR, exist_ok=True)

class TemporalMemory:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.lock = threading.Lock()
        self.daily_memory_file = f"{MEMORY_DIR}{agent_id}_daily.json"
        self.weekly_memory_file = f"{MEMORY_DIR}{agent_id}_weekly.json"
        self.load_memory()

    def load_memory(self):
        self.daily_memory = self._load_file(self.daily_memory_file)
        self.weekly_memory = self._load_file(self.weekly_memory_file)

    def _load_file(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                return data
        return {}

    def _save_file(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def update_memory(self, context, memory_type="daily"):
        now = datetime.now().isoformat()
        context['timestamp'] = now

        with self.lock:
            if memory_type == "daily":
                self.daily_memory[now] = context
                self._save_file(self.daily_memory_file, self.daily_memory)
            elif memory_type == "weekly":
                self.weekly_memory[now] = context
                self._save_file(self.weekly_memory_file, self.weekly_memory)

    def get_context_range(self, since_minutes_ago=60, memory_type="daily"):
        cutoff = datetime.now() - timedelta(minutes=since_minutes_ago)
        memory = self.daily_memory if memory_type == "daily" else self.weekly_memory
        results = []

        for timestamp, context in memory.items():
            ts_time = datetime.fromisoformat(context['timestamp'])
            if ts_time >= cutoff:
                results.append(context)
        return results

    def flush_old_memory(self, retention_days=7):
        cutoff = datetime.now() - timedelta(days=retention_days)
        with self.lock:
            self.daily_memory = {
                ts: ctx for ts, ctx in self.daily_memory.items()
                if datetime.fromisoformat(ctx['timestamp']) >= cutoff
            }
            self.weekly_memory = {
                ts: ctx for ts, ctx in self.weekly_memory.items()
                if datetime.fromisoformat(ctx['timestamp']) >= cutoff
            }
            self._save_file(self.daily_memory_file, self.daily_memory)
            self._save_file(self.weekly_memory_file, self.weekly_memory)

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
            "summary": self.task_engine.get_recent_activity_summary(),
            "timestamp": datetime.now().isoformat()
        }
        self.memory.update_memory(context, memory_type="daily")

    def sync_weekly_memory(self):
        print("[ContextScheduler] Syncing weekly memory")
        context = {
            "performance_score": self.task_engine.get_performance_score(),
            "task_trends": self.task_engine.analyze_trends(),
            "timestamp": datetime.now().isoformat()
        }
        self.memory.update_memory(context, memory_type="weekly")

    def flush_memory(self):
        print("[ContextScheduler] Flushing old memory")
        self.memory.flush_old_memory()

    def shutdown(self):
        self.scheduler.shutdown()

# File: tasks/task_engine.py

class TaskEngine:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.tasks = []

    def get_active_tasks(self):
        return [task for task in self.tasks if not task.get('completed', False)]

    def get_recent_activity_summary(self):
        return f"{len(self.tasks)} tasks handled in last cycle"

    def get_performance_score(self):
        completed = sum(1 for t in self.tasks if t.get("completed", False))
        total = len(self.tasks)
        return round((completed / total) * 100, 2) if total > 0 else 0

    def analyze_trends(self):
        return {
            "completed": sum(1 for t in self.tasks if t.get("completed", False)),
            "pending": sum(1 for t in self.tasks if not t.get("completed", False)),
        }
