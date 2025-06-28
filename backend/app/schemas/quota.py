from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class QuotaBase(BaseModel):
    resource: str
    limit: int
    used: Optional[int] = 0

class QuotaCreate(QuotaBase):
    organization_id: int

class QuotaOut(QuotaBase):
    id: int
    organization_id: int
    created_at: datetime

    class Config:
        orm_mode = True
