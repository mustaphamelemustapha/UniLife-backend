from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, EmailStr, StringConstraints

# ========= USER =========


PasswordStr = Annotated[str, StringConstraints(min_length=6, max_length=72)]


class UserCreate(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserRead(BaseModel):
    id: int
    email: EmailStr
    display_name: str | None = None
    avatar_url: str | None = None
    dark_mode: int | None = 0

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserProfileUpdate(BaseModel):
    display_name: str | None = None
    avatar_url: str | None = None
    dark_mode: int | None = 0


# ========= EXPENSE =========


class ExpenseCreate(BaseModel):
    category: str
    amount: float


class ExpenseRead(BaseModel):
    id: int
    category: str
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True


# ========= STUDY =========


class StudyPlanCreate(BaseModel):
    task: str
    day: str
    priority: str


class StudyPlanRead(BaseModel):
    id: int
    task: str
    day: str
    priority: str

    class Config:
        from_attributes = True


# ========= ADMIN =========


class AdminExpenseRead(BaseModel):
    id: int
    category: str
    amount: float
    created_at: datetime
    user_id: int
    user_email: EmailStr


class AdminStudyRead(BaseModel):
    id: int
    task: str
    day: str
    priority: str
    user_id: int
    user_email: EmailStr
