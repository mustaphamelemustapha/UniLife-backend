from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import study, expenses

app = FastAPI(title="UniLife Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(study.router, prefix="/study", tags=["Study"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])


@app.get("/")
def root():
    return {"message": "UniLife backend running"}
