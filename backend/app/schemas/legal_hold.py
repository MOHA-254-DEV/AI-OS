from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class LegalHoldBase(BaseModel):
    organization_id: int
    file_id: int
    active: Optional[bool] = True

class LegalHoldCreate(LegalHoldBase):
    pass

class LegalHoldOut(LegalHoldBase):
    id: int
    created_at: datetime
    released_at: Optional[datetime] = None

    class Config:
        orm_mode = True
