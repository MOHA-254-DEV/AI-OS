from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base

class FirewallRule(Base):
    __tablename__ = "firewall_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    direction = Column(Enum("inbound", "outbound", name="direction"), nullable=False)
    protocol = Column(String, nullable=False)
    port = Column(String, nullable=False)
    action = Column(Enum("allow", "deny", name="action"), nullable=False)
