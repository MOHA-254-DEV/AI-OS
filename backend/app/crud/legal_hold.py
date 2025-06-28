from sqlalchemy.orm import Session
from app.db.models.legal_hold import LegalHold
from app.schemas.legal_hold import LegalHoldCreate

def get_legal_hold(db: Session, hold_id: int):
    return db.query(LegalHold).filter(LegalHold.id == hold_id).first()

def get_legal_holds_for_org(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(LegalHold).filter(LegalHold.organization_id == organization_id).offset(skip).limit(limit).all()

def create_legal_hold(db: Session, hold: LegalHoldCreate):
    db_hold = LegalHold(
        organization_id=hold.organization_id,
        file_id=hold.file_id,
        active=hold.active
    )
    db.add(db_hold)
    db.commit()
    db.refresh(db_hold)
    return db_hold

def release_legal_hold(db: Session, db_hold: LegalHold):
    db_hold.active = False
    db.commit()
    db.refresh(db_hold)
    return db_hold

def delete_legal_hold(db: Session, db_hold: LegalHold):
    db.delete(db_hold)
    db.commit()
    return db_hold
