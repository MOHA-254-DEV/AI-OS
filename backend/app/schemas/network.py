from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NetworkBase(BaseModel):
    name: str
    cidr: str
    description: Optional[str] = None

class NetworkCreate(NetworkBase):
    organization_id: int

class NetworkOut(NetworkBase):
    id: int
    organization_id: int
    created_at: datetime

    class Config:
        orm_mode = True
