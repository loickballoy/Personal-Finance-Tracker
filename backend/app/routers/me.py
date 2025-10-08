from fastapi import APIRouter, Depends
from ..deps import get_current_user
from .. import schemas


router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=schemas.MeOut)
def me(user = Depends(get_current_user)):
    return schemas.MeOut(
        id=str(user["id"]),
        email=user["email"],
        full_name=user.get("full_name"),
        currency=user.get("currency", "EUR"),
        role=user.get("role", "user"),
    )