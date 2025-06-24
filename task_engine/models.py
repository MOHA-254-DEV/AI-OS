# task_engine/models.py
from pydantic import BaseModel
from typing import Optional, List

class TaskInput(BaseModel):
    id: str
    name: str
    agent: str
    urgency: int  # 1-10
    deadline: Optional[str] = None
    tags: Optional[List[str]] = []
    context: Optional[str] = None

class ScoredTask(BaseModel):
    id: str
    priority: float
    data: TaskInput
