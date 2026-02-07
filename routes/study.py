from fastapi import APIRouter, HTTPException, Body, Depends
from dependencies import get_current_user
from models.user import User
from pydantic import BaseModel
import json
import os

router = APIRouter(
    prefix="/study",
    tags=["Study"]
)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "../data/study.json"
)

# Ensure data directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


class Plan(BaseModel):
    task: str
    day: str
    priority: str


def load_plans():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_plans(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ================= GET ALL PLANS =================


@router.get("/")
def get_plans(current_user: User = Depends(get_current_user)):
    return load_plans()

# ================= ADD PLAN =================


@router.post("/")
def add_plan(plan: Plan, current_user: User = Depends(get_current_user)):
    plans = load_plans()
    plan_id = max([p.get("id", 0) for p in plans], default=0) + 1
    plan_dict = plan.dict()
    plan_dict["id"] = plan_id
    plans.append(plan_dict)
    save_plans(plans)
    return {"success": True, "id": plan_id}

# ================= UPDATE PLAN =================


@router.put("/{plan_id}")
def update_plan(plan_id: int, plan: Plan, current_user: User = Depends(get_current_user)):
    plans = load_plans()
    for p in plans:
        if p.get("id") == plan_id:
            p.update(plan.dict())
            save_plans(plans)
            return {"success": True}
    raise HTTPException(status_code=404, detail="Plan not found")

# ================= DELETE PLAN =================


@router.delete("/{plan_id}")
def delete_plan(plan_id: int, current_user: User = Depends(get_current_user)):
    plans = load_plans()
    new_plans = [p for p in plans if p.get("id") != plan_id]
    if len(new_plans) == len(plans):
        raise HTTPException(status_code=404, detail="Plan not found")
    save_plans(new_plans)
    return {"success": True}

# ================= RESET PLANS =================


@router.post("/reset/")
def reset_plans(plans: list[dict] = Body(...), current_user: User = Depends(get_current_user)):
    """
    Reset all plans. Accepts a JSON array of plans in the body.
    """
    save_plans(plans)
    return {"success": True}
