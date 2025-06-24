# File: tasks/task_engine.py

from typing import List, Dict

class TaskEngine:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.tasks: List[Dict] = []

    def add_task(self, task: Dict):
        self.tasks.append(task)

    def get_active_tasks(self) -> List[Dict]:
        return [task for task in self.tasks if not task.get('completed', False)]

    def get_recent_activity_summary(self) -> str:
        completed = sum(1 for task in self.tasks if task.get("completed", False))
        pending = len(self.tasks) - completed
        return f"{len(self.tasks)} total tasks | ✅ Completed: {completed} | ⏳ Pending: {pending}"

    def get_performance_score(self) -> float:
        total = len(self.tasks)
        if total == 0:
            return 0.0
        completed = sum(1 for t in self.tasks if t.get("completed", False))
        return round((completed / total) * 100, 2)

    def analyze_trends(self) -> Dict[str, int]:
        return {
            "completed": sum(1 for t in self.tasks if t.get("completed", False)),
            "pending": sum(1 for t in self.tasks if not t.get("completed", False)),
        }

    def reset_tasks(self):
        self.tasks.clear()

    def __repr__(self):
        return f"<TaskEngine agent={self.agent_id} tasks={len(self.tasks)}>"
