from fastapi import APIRouter
from pydantic import BaseModel
import os
import json

router = APIRouter()

# -------------------------
# DATA SETUP
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLANS_FILE = os.path.join(DATA_DIR, "plans.json")

os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(PLANS_FILE):
    with open(PLANS_FILE, "w") as f:
        json.dump([], f)

# -------------------------
# SCHEMA (THIS IS KEY)
# -------------------------


class StudyPlan(BaseModel):
    task: str
    day: str
    priority: str

# -------------------------
# HELPERS
# -------------------------


def load_plans():
    with open(PLANS_FILE, "r") as f:
        return json.load(f)


def save_plans(plans):
    with open(PLANS_FILE, "w") as f:
        json.dump(plans, f, indent=2)

# -------------------------
# ROUTES
# -------------------------


@router.get("/plans")
def get_plans():
    return load_plans()


@router.post("/plans")
def add_plan(plan: StudyPlan):
    plans = load_plans()
    plans.append(plan.dict())
    save_plans(plans)
    return {"status": "ok"}
