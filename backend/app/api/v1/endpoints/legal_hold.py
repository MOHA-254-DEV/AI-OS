from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.legal_hold import LegalHoldOut, LegalHoldCreate
from app.crud.legal_hold import get_legal_hold, get_legal_holds_for_org, create_legal_hold, release_legal_hold, delete_legal_hold
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[LegalHoldOut])
def list_legal_holds(organization_id: int, db: Session = Depends(get_db)):
    return get_legal_holds_for_org(db, organization_id=organization_id)

@router.get("/{hold_id}", response_model=LegalHoldOut)
def retrieve_legal_hold(hold_id: int, db: Session = Depends(get_db)):
    hold = get_legal_hold(db, hold_id)
    if not hold:
        raise HTTPException(status_code=404, detail="Legal hold not found")
    return hold

@router.post("/", response_model=LegalHoldOut)
def create_legal_hold_api(hold_in: LegalHoldCreate, db: Session = Depends(get_db)):
    return create_legal_hold(db, hold=hold_in)

@router.post("/{hold_id}/release", response_model=LegalHoldOut)
def release_legal_hold_api(hold_id: int, db: Session = Depends(get_db)):
    db_hold = get_legal_hold(db, hold_id)
    if not db_hold:
        raise HTTPException(status_code=404, detail="Legal hold not found")
    return release_legal_hold(db, db_hold)

@router.delete("/{hold_id}")
def delete_legal_hold_api(hold_id: int, db: Session = Depends(get_db)):
    db_hold = get_legal_hold(db, hold_id)
    if not db_hold:
        raise HTTPException(status_code=404, detail="Legal hold not found")
    return delete_legal_hold(db, db_hold)
