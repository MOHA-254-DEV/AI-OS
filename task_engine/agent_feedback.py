# task_engine/agent_feedback.py
import redis
import json
from models import ScoredTask
from prioritizer import score_task

r = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_KEY = "task_queue"

def update_feedback(agent_id: str, task_id: str, score: float):
    raw = r.get(f"task:{task_id}")
    if not raw:
        return {"error": "Task not found"}

    task_data = json.loads(raw)
    task_data["priority"] += score  # live tuning

    # Replace in queue
    r.zadd(QUEUE_KEY, {task_id: task_data["priority"]})
    r.set(f"task:{task_id}", json.dumps(task_data))
    return {"status": "updated", "new_score": task_data["priority"]}
