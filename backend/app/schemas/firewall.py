from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FirewallBase(BaseModel):
    rule_name: str
    action: str
    source: Optional[str] = None
    destination: Optional[str] = None
    protocol: Optional[str] = None
    is_active: Optional[bool] = True

class FirewallCreate(FirewallBase):
    organization_id: int

class FirewallOut(FirewallBase):
    id: int
    organization_id: int
    created_at: datetime

    class Config:
        orm_mode = True
