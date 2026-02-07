from typing import Annotated
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

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ========= EXPENSE =========


class ExpenseCreate(BaseModel):
    category: str
    amount: float


class ExpenseRead(BaseModel):
    id: int
    category: str
    amount: float

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
