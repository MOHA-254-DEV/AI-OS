from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FileBase(BaseModel):
    filename: str
    size: int
    is_deleted: Optional[bool] = False

class FileCreate(FileBase):
    owner_id: int
    organization_id: int
    path: str

class FileOut(FileBase):
    id: int
    owner_id: int
    organization_id: int
    path: str
    created_at: datetime

    class Config:
        orm_mode = True
