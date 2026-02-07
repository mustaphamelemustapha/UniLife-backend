from pydantic import BaseModel, EmailStr

# ========= USER =========


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


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
    title: str
    subject: str
    duration: int


class StudyPlanRead(BaseModel):
    id: int
    title: str
    subject: str
    duration: int

    class Config:
        from_attributes = True
