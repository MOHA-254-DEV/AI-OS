from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    message: str
    read: Optional[bool] = False

class NotificationCreate(NotificationBase):
    user_id: int
    organization_id: int

class NotificationOut(NotificationBase):
    id: int
    user_id: int
    organization_id: int
    created_at: datetime

    class Config:
        orm_mode = True
