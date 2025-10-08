from fastapi import APIRouter, Depends
from ..db import get_supabase, Client
from ..deps import get_current_user
from .. import schemas


router = APIRouter(prefix="/categories", tags=["categories"])


