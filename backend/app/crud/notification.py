from sqlalchemy.orm import Session
from app.db.models.notification import Notification
from app.schemas.notification import NotificationCreate

def get_notification(db: Session, notif_id: int):
    return db.query(Notification).filter(Notification.id == notif_id).first()

def get_notifications_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Notification).filter(Notification.user_id == user_id).offset(skip).limit(limit).all()

def create_notification(db: Session, notif: NotificationCreate):
    db_notif = Notification(
        message=notif.message,
        user_id=notif.user_id,
        organization_id=notif.organization_id,
        read=notif.read,
    )
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif

def mark_notification_read(db: Session, notif: Notification):
    notif.read = True
    db.commit()
    db.refresh(notif)
    return notif

def delete_notification(db: Session, notif: Notification):
    db.delete(notif)
    db.commit()
    return notif
