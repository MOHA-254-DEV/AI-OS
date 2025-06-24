# task_engine/prioritizer.py
from models import TaskInput
from datetime import datetime
import math

def score_task(task: TaskInput):
    urgency_weight = task.urgency
    tag_boost = len(task.tags or []) * 0.5

    # Bonus if deadline is near
    deadline_boost = 0
    if task.deadline:
        try:
            days_left = (datetime.fromisoformat(task.deadline) - datetime.now()).days
            deadline_boost = max(0, 10 - days_left)
        except:
            pass

    # Contextual matching logic (can plug in GPT/NLP later)
    context_score = 1.0 if task.context and "urgent" in task.context.lower() else 0.5

    total = urgency_weight + tag_boost + deadline_boost + context_score
    return round(total, 2)
