from fastapi import APIRouter, Depends, HTTPException, status
import jwt
import json

from app.models import Users, Bank
from app.utils import *
from app.settings import settings

UserRouter = APIRouter()

@UserRouter.post("/users/delete", tags=["User"])
async def delete_user(email: str) -> None:
    """
        Admin function to delete function. Should be usefulls for tests
    """
    try:
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=400, detail="This user does not exist")
        delete_user(email)
        return {"message": "Successfully Deleted User"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))