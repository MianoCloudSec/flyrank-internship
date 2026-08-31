from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

from app_v4.client import supabase

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials=Depends(bearer_scheme)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Access token required")

    token = credentials.credentials

    if token == "":
        raise HTTPException(status_code=401, detail="Access token required")

    try:
        result = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if result is None or result.user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"user": result.user, "token": token}