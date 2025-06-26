from sqlalchemy import Column, String, Enum, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum("admin", "agent", "user", name="userroles"), nullable=False, default="user")
    avatar_url = Column(String, nullable=True)
    registered = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    status = Column(Enum("active", "disabled", name="userstatus"), default="active", nullable=False)
    is_verified = Column(Boolean, default=False)

    files = relationship("File", back_populates="owner")
