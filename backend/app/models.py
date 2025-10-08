from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Numeric, Date, Boolean, func
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    pass


UUID_PK = mapped_column(default=uuid.uuid4, primary_key=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = UUID_PK
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text)
    full_name: Mapped[str | None]
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    role: Mapped[str] = mapped_column(String, default="user")
    current_allocation_model_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("allocation_models.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[uuid.UUID] = UUID_PK
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(Text)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[uuid.UUID] = UUID_PK
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str]
    type: Mapped[str]
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    initial_balance: Mapped[float] = mapped_column(Numeric(14,2), default=0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


class AllocationModel(Base):
    __tablename__ = "allocation_models"
    id: Mapped[uuid.UUID] = UUID_PK
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str]
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class AllocationBucket(Base):
    __tablename__ = "allocation_buckets"
    id: Mapped[uuid.UUID] = UUID_PK
    model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("allocation_models.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    code: Mapped[str | None]
    name: Mapped[str]
    ratio: Mapped[float] = mapped_column(Numeric(5,4))
    sort_order: Mapped[int] = mapped_column(default=0)
    color: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class Subcategory(Base):
    __tablename__ = "subcategories"
    id: Mapped[uuid.UUID] = UUID_PK
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    bucket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("allocation_buckets.id", ondelete="CASCADE"), index=True)
    name: Mapped[str]
    color: Mapped[str | None]
    icon: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[uuid.UUID] = UUID_PK
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), index=True)
    subcategory_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("subcategories.id", ondelete="SET NULL"))
    description: Mapped[str | None]
    amount: Mapped[float] = mapped_column(Numeric(14,2))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    date: Mapped[datetime]
    notes: Mapped[str | None]
    imported: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())