from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.audit_log import AuditLogOut, AuditLogCreate
from app.crud.audit_log import get_audit_log, get_audit_logs_for_org, create_audit_log, delete_audit_log
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[AuditLogOut])
def list_audit_logs(organization_id: int, db: Session = Depends(get_db)):
    return get_audit_logs_for_org(db, organization_id=organization_id)

@router.get("/{log_id}", response_model=AuditLogOut)
def retrieve_audit_log(log_id: int, db: Session = Depends(get_db)):
    log = get_audit_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log

@router.post("/", response_model=AuditLogOut)
def create_audit_log_api(log_in: AuditLogCreate, db: Session = Depends(get_db)):
    return create_audit_log(db, log=log_in)

@router.delete("/{log_id}")
def delete_audit_log_api(log_id: int, db: Session = Depends(get_db)):
    db_log = get_audit_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return delete_audit_log(db, db_log)
