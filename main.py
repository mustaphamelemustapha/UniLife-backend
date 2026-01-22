from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import study, expenses

app = FastAPI(title="UniLife Backend")

# CORS (so frontend on another origin can access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(study.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "UniLife backend running"}
