from typing import List
from pydantic import BaseModel


class StudyPlanCreate(BaseModel):
    title: str
    duration: int


class ExpenseCreate(BaseModel):
    title: str
    amount: int


class StudyPlan(BaseModel):
    id: int
    title: str
    subject: str
    duration: str
