from app.db import get_supabase
from app.models import Users
import hashlib

def get_user(email: str) -> Users | None:
    supabase = next(get_supabase())
    response = supabase.table('Users').select('*').eq('email', email).execute()
    return Users(**response.data[0]) if response.data else None

def delete_user(email: str) -> None:
    supabase = next(get_supabase())
    supabase.table('Users').delete().eq('email', email).execute()

def db_insert(user: Users) -> None:
    supabase = next(get_supabase())
    supabase.table('Users').insert(user.model_dump()).execute()

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def add_verification_token(created_user: Users, token: str) -> None:
    supabase = next(get_supabase())
    response = supabase.table('Users').select('*').eq('email', created_user.email).execute()
    payload = {
        "user_id": response.data[0]["uuid"],
        "token": token
    }
    supabase.table('verification_tokens').insert(payload).execute()

def update_verification_token(real_user: Users, token: str) -> None:
    supabase = next(get_supabase())
    response = supabase.table('Users').select('*').eq('email', real_user.email).execute()
    uuid = response.data[0]["uuid"]
    payload = {
        "user_id": uuid,
        "token": token
    }
    supabase.table('verification_tokens').update(payload).eq("user_id", uuid).execute()