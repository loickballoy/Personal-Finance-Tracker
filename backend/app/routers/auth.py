from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
import jwt
import json

from app.models import Users, Bank
from app.utils import *
from app.settings import settings

AuthRouter = APIRouter()

@AuthRouter.post("/auth/signup", tags=["Auth"])
async def signup(user: Users) -> dict[str, Any]:
    """
        Sign Up Function For our webapp. Creates an entry in our Supabase DB, 
        a JWT token that we save in another table and link it to the created user's uuid.
        Once All that is saved and created we send an E-mail to verify the user's email.
    """
    try:
        # Check If user exists
        existing_user = get_user(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        # Hash Password
        user.password = get_password_hash(user.password)
        # Add to supabase db
        db_insert(user)
        # Create JWT token
        created_user = get_user(user.email)
        payload = json.loads(created_user.model_dump_json())
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        add_verification_token(created_user, token)
        # Confirm e-mail
        # TODO
        
        return {"message": "User created successfully", "JWTtoken": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@AuthRouter.post("/auth/login", tags=["Auth"])
async def login(user: Users) -> dict[str, Any]:
    """
        Log In Function for our webapp. Updates the JWT token in our verification_token table.
        Also Returns the JWT token to be used by our Frontend and our other API operations.
    """
    try:
        real_user = get_user(user.email)
        if not real_user:
            raise HTTPException(status_code=400, detail="This user does not exist")
        isMatch = get_password_hash(user.password) == real_user.password
        if not isMatch:
            raise HTTPException(status_code=401, detail="Incorrect E-mail/Password")
        
        payload = json.loads(real_user.model_dump_json())
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        update_verification_token(real_user, token)

        return {"message": "Logged in Successfully", "JWTtoken": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

