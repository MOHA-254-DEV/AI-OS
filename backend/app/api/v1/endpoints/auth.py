from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.security import create_access_token
from app.core.config import settings
from app.core.email import send_email
from app.db.models.user import User
from app.schemas.user import UserOut
from app.api.deps import get_db
from app.crud.user import authenticate_user, get_user_by_email

router = APIRouter()

@router.post("/login", response_model=dict)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled"
        )
    token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": str(user.id)}, expires_delta=token_expires)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/reset-password", response_model=dict)
def reset_password(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Generate reset token (could be JWT, but keep it simple)
    from uuid import uuid4
    reset_token = str(uuid4())
    # Store token & send email (for demo: not stored in DB)
    reset_link = f"https://your-frontend-domain/reset-password?token={reset_token}"
    send_email(
        to_email=user.email,
        subject="Password Reset Request",
        body=f"Click to reset your password: {reset_link}"
    )
    return {"msg": "Password reset email sent."}
