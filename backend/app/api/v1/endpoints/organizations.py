from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.organization import OrganizationOut, OrganizationCreate, OrganizationUpdate
from app.crud.organization import get_organization, get_organizations, create_organization, update_organization, delete_organization, get_organization_by_name
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[OrganizationOut])
def list_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_organizations(db, skip=skip, limit=limit)

@router.get("/{org_id}", response_model=OrganizationOut)
def retrieve_organization(org_id: int, db: Session = Depends(get_db)):
    org = get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.post("/", response_model=OrganizationOut)
def create_organization_api(org_in: OrganizationCreate, db: Session = Depends(get_db)):
    if get_organization_by_name(db, org_in.name):
        raise HTTPException(status_code=400, detail="Organization already exists")
    return create_organization(db, org=org_in)

@router.patch("/{org_id}", response_model=OrganizationOut)
def update_organization_api(org_id: int, org_update: OrganizationUpdate, db: Session = Depends(get_db)):
    db_org = get_organization(db, org_id)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return update_organization(db, db_org, org_update)

@router.delete("/{org_id}")
def delete_organization_api(org_id: int, db: Session = Depends(get_db)):
    db_org = get_organization(db, org_id)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return delete_organization(db, db_org)
