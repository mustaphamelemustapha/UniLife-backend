from datetime import datetime, timedelta
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import Expense, User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()
    start_30 = now - timedelta(days=30)
    start_7 = now - timedelta(days=7)

    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()

    # Normalize missing created_at (older rows) to now
    for e in expenses:
        if e.created_at is None:
            e.created_at = now

    weekly_totals = defaultdict(float)
    monthly_totals = defaultdict(float)
    category_totals = defaultdict(float)

    for e in expenses:
        if e.created_at >= start_7:
            key = e.created_at.strftime("%a")
            weekly_totals[key] += e.amount
        if e.created_at >= start_30:
            key = e.created_at.strftime("%b %d")
            monthly_totals[key] += e.amount
            category_totals[e.category] += e.amount

    # Sort weekly by weekday order
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekly_series = [{"label": d, "value": round(weekly_totals.get(d, 0), 2)} for d in weekdays]

    # Sort monthly by date
    monthly_series = [{"label": k, "value": round(v, 2)} for k, v in monthly_totals.items()]

    category_series = [
        {"label": k, "value": round(v, 2)}
        for k, v in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "weekly": weekly_series,
        "monthly": monthly_series,
        "categories": category_series
    }
