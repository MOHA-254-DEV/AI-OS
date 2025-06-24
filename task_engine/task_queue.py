# task_engine/task_queue.py
import redis
import json
from models import TaskInput, ScoredTask
from prioritizer import score_task

r = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_KEY = "task_queue"

def add_task(task: TaskInput):
    score = score_task(task)
    scored = ScoredTask(id=task.id, priority=score, data=task)
    r.zadd(QUEUE_KEY, {task.id: score})
    r.set(f"task:{task.id}", scored.json())
    return {"status": "added", "score": score}

def list_tasks():
    task_ids = r.zrevrange(QUEUE_KEY, 0, -1)
    tasks = []
    for tid in task_ids:
        raw = r.get(f"task:{tid.decode()}")
        if raw:
            tasks.append(json.loads(raw))
    return tasks

def get_next_task():
    result = r.zrevrange(QUEUE_KEY, 0, 0)
    if not result:
        return {"task": None}
    task_id = result[0].decode()
    task_raw = r.get(f"task:{task_id}")
    if task_raw:
        r.zrem(QUEUE_KEY, task_id)
        return json.loads(task_raw)
    return {"task": None}
