from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter()

EXPENSES_FILE = "../frontend/expenses-tracker/expenses.json"


class Expense(BaseModel):
    name: str
    amount: float
    category: str


def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return []
    try:
        with open(EXPENSES_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_expenses(expenses):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


@router.get("/")
def get_expenses():
    return load_expenses()


@router.post("/")
def add_expense(expense: Expense):
    expenses = load_expenses()
    expenses.append(expense.dict())
    save_expenses(expenses)
    return {"success": True, "message": "Expense added!", "expense": expense.dict()}
