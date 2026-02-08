from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 👇 DATABASE
from database import engine
from database import Base, engine


# 👇 FORCE MODEL IMPORTS (VERY IMPORTANT)
from models.user import User
from models.expense import Expense
from models.study import StudyPlan
from models.password_reset import PasswordResetToken

# 👇 ROUTERS
from routes import expenses, study, auth, admin, password_reset, analytics

app = FastAPI(title="UniLife Backend", version="0.1.0")

# CORS: allow local frontend + Render domain. Adjust as needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CREATE DATABASE TABLES
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(study.router)
app.include_router(admin.router)
app.include_router(password_reset.router)
app.include_router(analytics.router)

# =========================
# Swagger JWT Configuration
# =========================


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="UniLife Backend API",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Protect auth/me + expenses + study + admin + analytics endpoints
    for path in openapi_schema["paths"]:
        if (
            path.startswith("/expenses")
            or path.startswith("/study")
            or path == "/me"
            or path.startswith("/admin")
            or path.startswith("/analytics")
        ):
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [
                    {"BearerAuth": []}
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
