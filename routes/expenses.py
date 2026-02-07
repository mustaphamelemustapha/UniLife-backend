from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Expense
from schemas import ExpenseCreate, ExpenseRead

router = APIRouter()


@router.get("/expenses/", response_model=list[ExpenseRead])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


@router.post("/expenses/", response_model=ExpenseRead)
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        user_id=1  # TEMP user (we’ll fix auth fully next)
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"detail": "Expense deleted"}


@router.post("/expenses/reset/")
def reset_expenses(db: Session = Depends(get_db)):
    db.query(Expense).delete()
    db.commit()
    return {"detail": "All expenses reset"}
