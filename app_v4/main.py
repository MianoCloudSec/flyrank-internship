from fastapi import FastAPI, HTTPException, Depends

from app_v4.client import supabase
from app_v4.models import AuthCredentials
from app_v4.dependencies import get_current_user

app = FastAPI(
    title="Auth API",
    description="A CRUD-adjacent API secured with Supabase Auth.",
    version="4.0",
)

print("Server running and connected to Supabase")


@app.post("/auth/signup", status_code=201)
def signup(credentials: AuthCredentials):
    if credentials.email == "" or credentials.password == "":
        raise HTTPException(status_code=400, detail="email and password are required")

    try:
        result = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password,
        })
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {"user": result.user}


@app.post("/auth/login")
def login(credentials: AuthCredentials):
    if credentials.email == "" or credentials.password == "":
        raise HTTPException(status_code=400, detail="email and password are required")

    try:
        result = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password,
        })
    except Exception as error:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token": result.session.access_token,
        "refresh_token": result.session.refresh_token,
    }


@app.post("/auth/logout", status_code=204)
def logout(current_user: dict = Depends(get_current_user)):
    token = current_user["token"]

    try:
        supabase.auth.sign_out(token)
    except Exception:
        pass

    return None


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(current_user: dict = Depends(get_current_user)):
    user = current_user["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }