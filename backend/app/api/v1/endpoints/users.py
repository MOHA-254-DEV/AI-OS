from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.crud.user import (
    create_user, get_user, get_users, update_user, delete_user
)
from app.api.deps import get_db, get_current_active_admin, get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin),
    skip: int = 0,
    limit: int = 100,
):
    return get_users(db, skip=skip, limit=limit)

@router.get("/me", response_model=UserOut)
def get_me(current_user = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserOut)
def create_new_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    if get_user(db, user_in.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return create_user(db, user_in)

@router.patch("/{user_id}", response_model=UserOut)
def update_user_info(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, db_user, user_update)

@router.delete("/{user_id}", response_model=dict)
def delete_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, db_user)
    return {"msg": "User deleted"}
