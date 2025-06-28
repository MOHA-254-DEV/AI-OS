from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.notification import NotificationOut, NotificationCreate
from app.crud.notification import get_notification, get_notifications_for_user, create_notification, mark_notification_read, delete_notification
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[NotificationOut])
def list_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_notifications_for_user(db, user_id=current_user.id)

@router.get("/{notif_id}", response_model=NotificationOut)
def retrieve_notification(notif_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    notif = get_notification(db, notif_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notif

@router.post("/", response_model=NotificationOut)
def create_notification_api(notif_in: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification(db, notif=notif_in)

@router.post("/{notif_id}/mark-read", response_model=NotificationOut)
def mark_read_api(notif_id: int, db: Session = Depends(get_db)):
    notif = get_notification(db, notif_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return mark_notification_read(db, notif)

@router.delete("/{notif_id}")
def delete_notification_api(notif_id: int, db: Session = Depends(get_db)):
    notif = get_notification(db, notif_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return delete_notification(db, notif)
