from sqlmodel import SQLModel, Field
from uuid import uuid4
from enum import Enum
from datetime import date, datetime, timezone


class TransactionStatus(Enum):
    BORROWED = "Borrowed"
    RETURNED = "Returned"


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    book_id: str = Field(foreign_key="books.id", nullable=False, ondelete="CASCADE")
    status: str = Field(
        default_factory=lambda: TransactionStatus.BORROWED.value, nullable=False
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    class Config:
        arbitrary_types_allowed = True
