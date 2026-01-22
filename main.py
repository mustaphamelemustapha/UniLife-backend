from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import study, expenses

app = FastAPI(title="UniLife Backend")

# ✅ CORS FIX (THIS IS THE KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(study.router, prefix="/study")
app.include_router(expenses.router, prefix="/expenses")


@app.get("/")
def root():
    return {"message": "UniLife backend running"}
