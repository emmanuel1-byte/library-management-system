from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import date, datetime, timezone


class Profile(SQLModel, table=True):

    __tablename__ = "profiles"

    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    profile_picture: str = Field(nullable=True)
    cover_picture: str = Field(nullable=True)
    bio: str = Field(nullable=True)
    user_id: str = Field(unique=True, foreign_key="users.id")
    created_at: date = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: date = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    class Config:
        arbitrary_types_allowed = True
