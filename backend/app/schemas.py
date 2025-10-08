from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


# ===== Auth =====
class SignupIn(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MeOut(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str]
    currency: str
    role: str

# ===== Categories =====
class CategoryIn(BaseModel):
    name: str


# ===== Subcategories =====
class SubcategoryIn(BaseModel):
    bucket_id: str
    name: str
    color: Optional[str] = None
    icon: Optional[str] = None


class SubcategoryOut(SubcategoryIn):
    id: str


# ===== Transactions =====
class TransactionIn(BaseModel):
    account_id: str
    subcategory_id: Optional[str] = None
    description: Optional[str] = None
    amount: Decimal
    currency: str = "EUR"
    date: date
    notes: Optional[str] = None


class TransactionOut(TransactionIn):
    id: str
    created_at: datetime
    updated_at: datetime