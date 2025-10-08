from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta, timezone
from ..db import get_supabase, Client
from .. import schemas, security
from ..jwt_utils import create_access_token, create_refresh_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.TokenPair)
def signup(payload: schemas.SignupIn, supabase: Client = Depends(get_supabase)):
    # 1) email unique ?
    existing = supabase.table("users").select("id").eq("email", payload.email).limit(1).execute().data
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")


    # 2) insert user
    user_row = {
        "email": payload.email,
        "password_hash": security.hash_password(payload.password),
        "full_name": payload.full_name,
    }
    ins = supabase.table("users").insert(user_row).execute()
    if ins.data and "id" in ins.data[0]:
        user_id = ins.data[0]["id"]
    else:
        sel = supabase.table("users").select("id").eq("email", payload.email).limit(1).execute()
        if not sel.data:
            raise HTTPException(status_code=500, detail="Failed to create user")
        user_id = sel.data[0]["id"]


    # 3) tokens + refresh storage
    access = create_access_token(str(user_id))
    refresh = create_refresh_token(str(user_id))
    supabase.table("refresh_tokens").insert({
        "user_id": user_id,
        "token_hash": security.hash_password(refresh),
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat()
    }).execute()


    return {"access_token": access, "refresh_token": refresh}


@router.post("/login", response_model=schemas.TokenPair)
def login(payload: schemas.LoginIn, supabase: Client = Depends(get_supabase)):
    res = supabase.table("users").select("id,password_hash").eq("email", payload.email).limit(1).execute()
    rows = res.data or []
    if not rows or not security.verify_password(payload.password, rows[0]["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = rows[0]["id"]


    access = create_access_token(str(user_id))
    refresh = create_refresh_token(str(user_id))
    supabase.table("refresh_tokens").insert({
        "user_id": user_id,
        "token_hash": security.hash_password(refresh),
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat()
    }).execute()


    return {"access_token": access, "refresh_token": refresh}