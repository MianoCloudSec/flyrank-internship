import os
from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
from supabase import create_client, Client

from app_v4.models import AuthCredentials

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(request: Request):
    auth_header = request.headers.get("Authorization")

    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")

    token = auth_header.removeprefix("Bearer ")

    if token == "":
        raise HTTPException(status_code=401, detail="Access token required")

    try:
        result = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if result is None or result.user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = result.user

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }