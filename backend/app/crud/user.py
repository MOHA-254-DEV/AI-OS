from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.session import Base

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False, index=True)
    type = Column(Enum("file", "folder", name="filetype"), nullable=False, default="file")
    size = Column(Integer, default=0)
    modified = Column(DateTime, default=datetime.utcnow)
    preview_url = Column(String, nullable=True)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")
