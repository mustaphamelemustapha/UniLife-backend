import os
import secrets
import hashlib
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import resend

from database import get_db
from models.user import User
from models.password_reset import PasswordResetToken
from passlib.context import CryptContext

router = APIRouter(prefix="/password-reset", tags=["Password Reset"])

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM = os.getenv("RESEND_FROM", "onboarding@resend.dev")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")
TOKEN_TTL_MINUTES = int(os.getenv("RESET_TOKEN_TTL_MINUTES", "30"))

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@router.post("/request")
def request_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    # Always respond OK to avoid user enumeration
    if not user:
        return {"success": True}

    if not RESEND_API_KEY:
        raise HTTPException(status_code=500, detail="Email service not configured")

    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)
    expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_TTL_MINUTES)

    db.add(PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        used=False
    ))
    db.commit()

    reset_link = f"{FRONTEND_BASE_URL}/auth/reset.html?token={token}"
    resend.api_key = RESEND_API_KEY
    resend.Emails.send({
        "from": RESEND_FROM,
        "to": [user.email],
        "subject": "Reset your UniLife password",
        "html": f"""
        <p>Hello,</p>
        <p>You requested a password reset for UniLife.</p>
        <p><a href='{reset_link}'>Click here to reset your password</a></p>
        <p>This link expires in {TOKEN_TTL_MINUTES} minutes.</p>
        """
    })

    return {"success": True}


@router.post("/confirm")
def confirm_reset(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    token_hash = hash_token(payload.token)
    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.used == False
    ).first()

    if not reset or reset.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    user.password = pwd_context.hash(payload.new_password)
    reset.used = True
    db.commit()
    return {"success": True}
