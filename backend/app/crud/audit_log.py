from sqlalchemy.orm import Session
from app.db.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate

def get_audit_log(db: Session, log_id: int):
    return db.query(AuditLog).filter(AuditLog.id == log_id).first()

def get_audit_logs_for_org(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(AuditLog).filter(AuditLog.organization_id == organization_id).offset(skip).limit(limit).all()

def create_audit_log(db: Session, log: AuditLogCreate):
    db_log = AuditLog(
        action=log.action,
        user_id=log.user_id,
        organization_id=log.organization_id,
        detail=log.detail,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def delete_audit_log(db: Session, db_log: AuditLog):
    db.delete(db_log)
    db.commit()
    return db_log
