from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class FileBase(BaseModel):
    name: str
    path: str
    type: str
    size: Optional[int] = 0
    modified: Optional[datetime] = None
    preview_url: Optional[str] = None

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    name: Optional[str]
    path: Optional[str]
    type: Optional[str]
    size: Optional[int]
    preview_url: Optional[str]

class FileOut(FileBase):
    id: uuid.UUID
    owner_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
