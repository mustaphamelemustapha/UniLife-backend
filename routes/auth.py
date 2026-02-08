from passlib.context import CryptContext
from schemas import UserCreate, UserLogin, Token, UserRead, UserProfileUpdate
from models.user import User
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jwt_utils import create_access_token
from dependencies import get_current_user

# Use a builtin hash to avoid bcrypt backend issues on Render
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

router = APIRouter()


# Hash password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# REGISTER
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# LOGIN
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# CURRENT USER
@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/profile", response_model=UserRead)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserRead)
def update_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.display_name is not None:
        current_user.display_name = payload.display_name
    if payload.avatar_url is not None:
        current_user.avatar_url = payload.avatar_url
    if payload.dark_mode is not None:
        current_user.dark_mode = payload.dark_mode
    db.commit()
    db.refresh(current_user)
    return current_user
