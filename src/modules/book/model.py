from sqlmodel import SQLModel, Field, Column, JSON
from uuid import uuid4
from typing import List
from datetime import date, datetime, timezone


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)

    title: str = Field(unique=True, nullable=False)
    author: List[str] = Field(sa_column=Column(JSON))
    genre: str
    isbn: str
    file_url: str = Field(nullable=True)
    available_copies: int
    total_copies: int
    created_at: date = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: date = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    class Config:
        arbitrary_types_allowed = True
