from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None

class OrganizationOut(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
