from typing import Annotated
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status

from app.models import Users, Bank
from app.utils import get_user, db_insert, get_password_hash

from app.routers.auth import AuthRouter
from app.routers.user import UserRouter

app = FastAPI()

@app.get('/')
async def hello_world():
    return {"message": "Hello World"}

app.include_router(AuthRouter)
app.include_router(UserRouter)
