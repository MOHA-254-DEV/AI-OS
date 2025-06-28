from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "member"
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    organization_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
