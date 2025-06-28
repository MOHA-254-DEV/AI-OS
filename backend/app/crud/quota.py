from sqlalchemy.orm import Session
from app.db.models.quota import Quota
from app.schemas.quota import QuotaCreate

def get_quota(db: Session, quota_id: int):
    return db.query(Quota).filter(Quota.id == quota_id).first()

def get_quotas_for_org(db: Session, organization_id: int):
    return db.query(Quota).filter(Quota.organization_id == organization_id).all()

def create_quota(db: Session, input: QuotaCreate):
    db_quota = Quota(
        organization_id=input.organization_id,
        resource=input.resource,
        limit=input.limit,
        used=input.used or 0
    )
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota)
    return db_quota

def update_quota_usage(db: Session, db_quota: Quota, used: int):
    db_quota.used = used
    db.commit()
    db.refresh(db_quota)
    return db_quota

def delete_quota(db: Session, db_quota: Quota):
    db.delete(db_quota)
    db.commit()
    return db_quota
