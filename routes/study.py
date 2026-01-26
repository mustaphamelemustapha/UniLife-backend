from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter(
    prefix="/study",
    tags=["Study"]
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "study.json")

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


class StudyPlan(BaseModel):
    task: str
    day: str
    priority: str


@router.get("/")
def get_plans():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


@router.post("/")
def add_plan(plan: StudyPlan):
    with open(DATA_FILE, "r") as f:
        plans = json.load(f)

    plans.append(plan.dict())

    with open(DATA_FILE, "w") as f:
        json.dump(plans, f, indent=2)

    return {"success": True}
