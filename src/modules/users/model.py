from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime, timezone
from enum import Enum
from typing import List
from sqlalchemy import Column, JSON


class Role(Enum):
    ADMIN = "Admin"
    MEMBER = "Member"


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    fullname: str
    email: str = Field(index=True, unique=True)
    password: str
    roles: List[str] = Field(
        default_factory=lambda: [Role.MEMBER.value], sa_column=Column(JSON)
    )
    verified: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    class Config:
        arbitrary_types_allowed = True
