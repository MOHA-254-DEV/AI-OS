from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate, org_id: int = None):
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        hashed_password=hash_password(user.password),
        is_active=True,
        is_superuser=user.is_superuser,
        organization_id=org_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_update: UserUpdate):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return db_user
