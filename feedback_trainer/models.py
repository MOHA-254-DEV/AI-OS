# feedback_trainer/models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FeedbackInput(BaseModel):
    task_id: str
    agent_id: str
    success: bool
    rating: Optional[int] = None  # 1–5
    comment: Optional[str] = ""
    correction: Optional[str] = ""
    timestamp: datetime = datetime.utcnow()

class CorrectionRecord(BaseModel):
    id: str
    original_output: str
    corrected_output: str
    context: Optional[str]
    timestamp: datetime = datetime.utcnow()
