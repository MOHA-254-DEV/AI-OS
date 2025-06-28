from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.firewall import FirewallOut, FirewallCreate
from app.crud.firewall import get_firewall, get_firewalls_for_org, create_firewall, update_firewall, delete_firewall
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[FirewallOut])
def list_firewalls(organization_id: int, db: Session = Depends(get_db)):
    return get_firewalls_for_org(db, organization_id=organization_id)

@router.get("/{fw_id}", response_model=FirewallOut)
def retrieve_firewall(fw_id: int, db: Session = Depends(get_db)):
    fw = get_firewall(db, fw_id)
    if not fw:
        raise HTTPException(status_code=404, detail="Firewall rule not found")
    return fw

@router.post("/", response_model=FirewallOut)
def create_firewall_api(fw_in: FirewallCreate, db: Session = Depends(get_db)):
    return create_firewall(db, fw=fw_in)

@router.patch("/{fw_id}", response_model=FirewallOut)
def update_firewall_api(fw_id: int, update_data: dict, db: Session = Depends(get_db)):
    db_fw = get_firewall(db, fw_id)
    if not db_fw:
        raise HTTPException(status_code=404, detail="Firewall rule not found")
    return update_firewall(db, db_fw, update_data)

@router.delete("/{fw_id}")
def delete_firewall_api(fw_id: int, db: Session = Depends(get_db)):
    db_fw = get_firewall(db, fw_id)
    if not db_fw:
        raise HTTPException(status_code=404, detail="Firewall rule not found")
    return delete_firewall(db, db_fw)
