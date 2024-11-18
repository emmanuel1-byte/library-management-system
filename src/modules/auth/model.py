from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime, timezone
from enum import Enum


class Role(Enum):
    ADMIN = "Admin"
    MEMBER = "Member"


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    fullname: str
    email: str = Field(index=True, unique=True)
    password: str
    role: Role = Field(default=Role.MEMBER)
    verified: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    class Config:
        arbitrary_types_allowed = True
