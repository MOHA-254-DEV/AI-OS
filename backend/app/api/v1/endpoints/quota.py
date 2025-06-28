from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.quota import QuotaOut, QuotaCreate
from app.crud.quota import get_quota, get_quotas_for_org, create_quota, update_quota_usage, delete_quota
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[QuotaOut])
def list_quotas(organization_id: int, db: Session = Depends(get_db)):
    return get_quotas_for_org(db, organization_id=organization_id)

@router.get("/{quota_id}", response_model=QuotaOut)
def retrieve_quota(quota_id: int, db: Session = Depends(get_db)):
    quota = get_quota(db, quota_id)
    if not quota:
        raise HTTPException(status_code=404, detail="Quota not found")
    return quota

@router.post("/", response_model=QuotaOut)
def create_quota_api(quota_in: QuotaCreate, db: Session = Depends(get_db)):
    return create_quota(db, input=quota_in)

@router.patch("/{quota_id}/used", response_model=QuotaOut)
def update_quota_usage_api(quota_id: int, used: int, db: Session = Depends(get_db)):
    db_quota = get_quota(db, quota_id)
    if not db_quota:
        raise HTTPException(status_code=404, detail="Quota not found")
    return update_quota_usage(db, db_quota, used)

@router.delete("/{quota_id}")
def delete_quota_api(quota_id: int, db: Session = Depends(get_db)):
    db_quota = get_quota(db, quota_id)
    if not db_quota:
        raise HTTPException(status_code=404, detail="Quota not found")
    return delete_quota(db, db_quota)
