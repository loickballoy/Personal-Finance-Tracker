import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from .settings import settings


ALG = settings.jwt_alg
SECRET = settings.jwt_secret


def create_access_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_min)
    payload: Dict[str, Any] = {"sub": sub, "type": "access", "exp": expire}
    return jwt.encode(payload, SECRET, algorithm=ALG)


def create_refresh_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expires_days)
    payload: Dict[str, Any] = {"sub": sub, "type": "refresh", "exp": expire}
    return jwt.encode(payload, SECRET, algorithm=ALG)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALG])