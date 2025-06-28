from sqlalchemy.orm import Session
from app.db.models.firewall import Firewall
from app.schemas.firewall import FirewallCreate

def get_firewall(db: Session, fw_id: int):
    return db.query(Firewall).filter(Firewall.id == fw_id).first()

def get_firewalls_for_org(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(Firewall).filter(Firewall.organization_id == organization_id).offset(skip).limit(limit).all()

def create_firewall(db: Session, fw: FirewallCreate):
    db_fw = Firewall(
        rule_name=fw.rule_name,
        action=fw.action,
        source=fw.source,
        destination=fw.destination,
        protocol=fw.protocol,
        is_active=fw.is_active,
        organization_id=fw.organization_id,
    )
    db.add(db_fw)
    db.commit()
    db.refresh(db_fw)
    return db_fw

def update_firewall(db: Session, db_fw: Firewall, update_data: dict):
    for field, value in update_data.items():
        setattr(db_fw, field, value)
    db.commit()
    db.refresh(db_fw)
    return db_fw

def delete_firewall(db: Session, db_fw: Firewall):
    db.delete(db_fw)
    db.commit()
    return db_fw
