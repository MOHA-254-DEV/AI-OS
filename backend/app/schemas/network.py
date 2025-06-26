from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class NetworkInterfaceBase(BaseModel):
    interface: str
    ip: Optional[str] = None
    mac: Optional[str] = None
    type: str
    ssid: Optional[str] = None
    status: str
    signal_strength: Optional[int] = None
    speed_mbps: Optional[int] = None

class NetworkInterfaceCreate(NetworkInterfaceBase):
    pass

class NetworkInterfaceUpdate(BaseModel):
    ip: Optional[str]
    mac: Optional[str]
    status: Optional[str]
    signal_strength: Optional[int]
    speed_mbps: Optional[int]

class NetworkInterfaceOut(NetworkInterfaceBase):
    id: uuid.UUID
    created: datetime

    class Config:
        orm_mode = True
