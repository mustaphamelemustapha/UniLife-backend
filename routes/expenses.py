from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# ================== DATA STRUCTURE ==================
# In-memory storage
expenses = []
next_id = 1  # auto-increment id for each expense

# ================== MODELS ==================


class Expense(BaseModel):
    amount: float
    category: str


class ExpenseOut(Expense):
    id: int

# ================== GET ALL EXPENSES ==================


@router.get("/expenses/", response_model=List[ExpenseOut])
def get_expenses():
    return expenses

# ================== ADD EXPENSE ==================


@router.post("/expenses/", response_model=ExpenseOut)
def add_expense(expense: Expense):
    global next_id
    exp_dict = expense.dict()
    exp_dict["id"] = next_id
    next_id += 1
    expenses.append(exp_dict)
    return exp_dict

# ================== DELETE EXPENSE ==================


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    global expenses
    for exp in expenses:
        if exp["id"] == expense_id:
            expenses = [e for e in expenses if e["id"] != expense_id]
            return {"message": "Expense deleted"}
    raise HTTPException(status_code=404, detail="Expense not found")

# ================== RESET EXPENSES ==================


@router.post("/reset")
def reset_expenses():
    global expenses, next_id
    expenses = []
    next_id = 1
    return {"message": "All expenses reset"}
