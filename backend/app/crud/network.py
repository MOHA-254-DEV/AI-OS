from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models.network import NetworkInterface
from app.schemas.network import NetworkInterfaceCreate, NetworkInterfaceUpdate

def get_interface(db: Session, interface_id):
    return db.query(NetworkInterface).filter(NetworkInterface.id == interface_id).first()

def get_interfaces(db: Session, skip: int = 0, limit: int = 100) -> List[NetworkInterface]:
    return db.query(NetworkInterface).offset(skip).limit(limit).all()

def create_interface(db: Session, interface: NetworkInterfaceCreate):
    db_interface = NetworkInterface(**interface.dict())
    db.add(db_interface)
    db.commit()
    db.refresh(db_interface)
    return db_interface

def update_interface(db: Session, db_interface: NetworkInterface, interface_update: NetworkInterfaceUpdate):
    for field, value in interface_update.dict(exclude_unset=True).items():
        setattr(db_interface, field, value)
    db.commit()
    db.refresh(db_interface)
    return db_interface

def delete_interface(db: Session, db_interface: NetworkInterface):
    db.delete(db_interface)
    db.commit()
    return True
