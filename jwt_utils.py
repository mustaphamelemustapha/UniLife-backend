import os
from datetime import datetime, timedelta

import jwt

# NOTE: Keep this secret >= 32 chars. Prefer setting via env var.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-me-please-32-chars-minimum-secret-key"
)
if len(SECRET_KEY) < 32:
    raise ValueError("SECRET_KEY must be at least 32 characters")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
