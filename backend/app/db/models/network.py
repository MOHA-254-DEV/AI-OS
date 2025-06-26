from sqlalchemy import Column, String, Integer, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.session import Base

class NetworkInterface(Base):
    __tablename__ = "network_interfaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    interface = Column(String, nullable=False)
    ip = Column(String, nullable=True)
    mac = Column(String, nullable=True)
    type = Column(String, nullable=False)  # ethernet, wifi, etc.
    ssid = Column(String, nullable=True)
    status = Column(String, nullable=False)  # connected, disconnected
    signal_strength = Column(Integer, nullable=True)
    speed_mbps = Column(Integer, nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
