import os
from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
import resend

from database import get_db
from models import StudyPlan, User

router = APIRouter(prefix="/reminders", tags=["Reminders"])

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM = os.getenv("RESEND_FROM", "onboarding@resend.dev")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")
REMINDER_SECRET = os.getenv("REMINDER_SECRET")


@router.post("/run")
def run_reminders(
    db: Session = Depends(get_db),
    x_reminder_secret: str | None = Header(default=None)
):
    if not REMINDER_SECRET or x_reminder_secret != REMINDER_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not RESEND_API_KEY:
        raise HTTPException(status_code=500, detail="Email service not configured")

    resend.api_key = RESEND_API_KEY
    now = datetime.utcnow()

    due = (
        db.query(StudyPlan, User)
        .join(User, StudyPlan.user_id == User.id)
        .filter(StudyPlan.remind_at != None)
        .filter(StudyPlan.remind_at <= now)
        .filter(StudyPlan.reminder_sent == False)
        .all()
    )

    for plan, user in due:
        resend.Emails.send({
            "from": RESEND_FROM,
            "to": [user.email],
            "subject": "UniLife Study Reminder",
            "html": f"""
            <p>Hi {user.display_name or user.email},</p>
            <p>This is a reminder for your study task:</p>
            <p><strong>{plan.task}</strong></p>
            <p>Scheduled: {plan.date} {plan.time}</p>
            <p><a href='{FRONTEND_BASE_URL}/dashboard/index.html'>Open UniLife</a></p>
            """
        })
        plan.reminder_sent = True
        plan.reminder_sent_at = now

    db.commit()
    return {"sent": len(due)}
