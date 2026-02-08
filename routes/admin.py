from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_admin
from models import User, Expense, StudyPlan
from schemas import UserRead, AdminExpenseRead, AdminStudyRead

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users", response_model=list[UserRead])
def list_users(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return db.query(User).order_by(User.id.desc()).all()


@router.get("/expenses", response_model=list[AdminExpenseRead])
def list_expenses(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    rows = (
        db.query(Expense, User)
        .join(User, Expense.user_id == User.id)
        .order_by(Expense.id.desc())
        .all()
    )
    return [
        {
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount,
            "created_at": expense.created_at,
            "user_id": user.id,
            "user_email": user.email
        }
        for expense, user in rows
    ]


@router.get("/study", response_model=list[AdminStudyRead])
def list_study_plans(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    rows = (
        db.query(StudyPlan, User)
        .join(User, StudyPlan.user_id == User.id)
        .order_by(StudyPlan.id.desc())
        .all()
    )
    return [
        {
            "id": plan.id,
            "task": plan.task,
            "day": plan.day,
            "priority": plan.priority,
            "user_id": user.id,
            "user_email": user.email
        }
        for plan, user in rows
    ]
