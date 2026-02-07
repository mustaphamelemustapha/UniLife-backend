from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Expense, User
from schemas import ExpenseCreate, ExpenseRead
from dependencies import get_current_user  # your JWT dependency

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# GET all expenses for the logged-in user


@router.get("/", response_model=list[ExpenseRead])
def get_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Expense).filter(Expense.user_id == current_user.id).all()

# ADD expense for the logged-in user


@router.post("/", response_model=ExpenseRead)
def add_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_expense = Expense(
        category=expense.category,
        amount=expense.amount,
        user_id=current_user.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# DELETE an expense (only if it belongs to the user)


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"detail": "Expense deleted"}

# RESET all expenses for the logged-in user


@router.post("/reset/")
def reset_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(Expense).filter(Expense.user_id == current_user.id).delete()
    db.commit()
    return {"detail": "All your expenses have been reset"}
