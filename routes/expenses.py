from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter(prefix="/expenses", tags=["Expenses"])

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "expenses.json")

# Ensure data folder & file exist
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


class Expense(BaseModel):
    amount: float
    category: str


def load_expenses():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_expenses(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@router.get("/")
def get_expenses():
    return load_expenses()


@router.post("/")
def add_expense(expense: Expense):
    expenses = load_expenses()
    expenses.append(expense.dict())
    save_expenses(expenses)
    return {"success": True}
