from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserOut, UserUpdate
from app.crud.user import get_user, get_users, update_user, delete_user
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserOut)
def update_user_api(user_id: int, update: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, db_user, update)

@router.delete("/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db, db_user)
