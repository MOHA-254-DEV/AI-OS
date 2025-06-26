from pydantic import BaseModel
from typing import Optional
import uuid

class FirewallRuleBase(BaseModel):
    name: str
    direction: str
    protocol: str
    port: str
    action: str

class FirewallRuleCreate(FirewallRuleBase):
    pass

class FirewallRuleUpdate(BaseModel):
    name: Optional[str]
    direction: Optional[str]
    protocol: Optional[str]
    port: Optional[str]
    action: Optional[str]

class FirewallRuleOut(FirewallRuleBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
