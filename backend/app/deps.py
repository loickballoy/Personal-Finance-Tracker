from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .db import get_supabase, Client
from .jwt_utils import decode_token


bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    supabase: Client = Depends(get_supabase),
):
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_token(creds.credentials)
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    res = supabase.table("users"). select("id,email,full_name,currency,role").eq("id", user_id).limit(1).execute()
    data = (res.data or [])
    if not data:
        raise HTTPException(status_code=401, detail="User not found")
    return data[0]