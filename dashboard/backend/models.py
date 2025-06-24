# dashboard/backend/models.py
from pydantic import BaseModel
from typing import Optional

class Goal(BaseModel):
    agent_id: str
    agent_name: str
    description: str
    deadline: str
    progress: int  # 0 to 100

class StrategyUpdate(BaseModel):
    strategy: str
