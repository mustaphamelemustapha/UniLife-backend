from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_current_user
from database import get_db
from models import StudyPlan, User
from schemas import StudyPlanCreate, StudyPlanRead

router = APIRouter(
    prefix="/study",
    tags=["Study"]
)

# ================= GET ALL PLANS =================


@router.get("/", response_model=list[StudyPlanRead])
def get_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(StudyPlan).filter(StudyPlan.user_id == current_user.id).all()

# ================= ADD PLAN =================


@router.post("/", response_model=StudyPlanRead)
def add_plan(
    plan: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_plan = StudyPlan(
        task=plan.task,
        day=plan.day,
        priority=plan.priority,
        date=plan.date,
        time=plan.time,
        user_id=current_user.id
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

# ================= UPDATE PLAN =================


@router.put("/{plan_id}", response_model=StudyPlanRead)
def update_plan(
    plan_id: int,
    plan: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db_plan.task = plan.task
    db_plan.day = plan.day
    db_plan.priority = plan.priority
    db_plan.date = plan.date
    db_plan.time = plan.time
    db.commit()
    db.refresh(db_plan)
    return db_plan

# ================= DELETE PLAN =================


@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(db_plan)
    db.commit()
    return {"success": True}

# ================= RESET PLANS =================


@router.post("/reset/")
def reset_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(StudyPlan).filter(StudyPlan.user_id == current_user.id).delete()
    db.commit()
    return {"success": True}
