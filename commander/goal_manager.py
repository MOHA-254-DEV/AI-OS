# commander/goal_manager.py

from queue import PriorityQueue
import uuid
import time
import threading
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Goal:
    def __init__(self, description: str, priority: int = 5):
        self.id = str(uuid.uuid4())
        self.description = description
        self.priority = priority
        self.created_at = time.time()
        self.completed = False
        self.completed_at = None

    def __lt__(self, other):
        # Max-Heap simulation: Higher priority is "less than"
        if not isinstance(other, Goal):
            raise TypeError(f"Cannot compare Goal with {type(other)}")
        return self.priority > other.priority

    def __repr__(self):
        return (
            f"Goal(id={self.id}, description='{self.description}', "
            f"priority={self.priority}, completed={self.completed})"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "created_at": self.created_at,
            "completed": self.completed,
            "completed_at": self.completed_at
        }


class GoalManager:
    def __init__(self):
        self._queue = PriorityQueue()
        self._completed_goals = []
        self._lock = threading.Lock()

    def add_goal(self, description: str, priority: int = 5) -> Goal:
        with self._lock:
            goal = Goal(description, priority)
            self._queue.put(goal)
            logger.info(f"[GOAL MANAGER] 🆕 Added new goal: {goal}")
            return goal

    def get_next_goal(self) -> Goal:
        with self._lock:
            if not self._queue.empty():
                goal = self._queue.get()
                logger.info(f"[GOAL MANAGER] 🎯 Retrieved goal: {goal}")
                return goal
            else:
                logger.info("[GOAL MANAGER] 📭 No goals available in the queue.")
                return None

    def mark_completed(self, goal: Goal):
        with self._lock:
            goal.completed = True
            goal.completed_at = time.time()
            self._completed_goals.append(goal)
            logger.info(f"[GOAL MANAGER] ✅ Goal marked as completed: {goal}")

    def list_completed_goals(self) -> list:
        with self._lock:
            return [g.to_dict() for g in self._completed_goals]

    def goals_pending(self) -> int:
        with self._lock:
            return self._queue.qsize()

    def total_completed(self) -> int:
        with self._lock:
            return len(self._completed_goals)

    def clear_all_goals(self):
        with self._lock:
            while not self._queue.empty():
                self._queue.get()
            self._completed_goals.clear()
            logger.info("[GOAL MANAGER] ♻️ Cleared all goals and completed records.")
