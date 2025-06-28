from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Firewall(Base):
    __tablename__ = "firewalls"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    rule_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    source = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    protocol = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization")
