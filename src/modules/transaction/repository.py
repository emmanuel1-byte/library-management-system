from sqlmodel import Session, select, func, and_
from src import Book
from .model import Transaction, TransactionStatus
from fastapi.encoders import jsonable_encoder
import math
from datetime import datetime, timezone
from ...utils.logger import logger


def find_book_by_id(book_id: str, session: Session):
    try:
        book__query = select(Book).where(Book.id == book_id)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        return jsonable_encoder(book)
    except Exception as e:
        logger.error(f"Error finding book: {e}")
        raise


def update_available_copies(book_id: str, increment: bool, session: Session):
    try:
        book_query = select(Book).where(Book.id == book_id)
        result = session.exec(book_query)

        book = result.one_or_none()

        if increment:
            book.available_copies += 1
        else:
            book.available_copies -= 1

        book.updated_at = datetime.now(timezone.utc).isoformat()

        session.add(book)
        session.commit()
        session.refresh(book)

        return book
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating available copies: {e}")
        raise


def create_transaction(user_id: str, book_id: str, session: Session):
    try:
        new_transaction = Transaction(user_id=user_id, book_id=book_id)

        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)

        return new_transaction
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating transaction: {e}")
        raise


def find_transaction(user_id: str, book_id: str, session: Session):
    try:
        transaction_query = select(Transaction).where(
            and_(Transaction.user_id == user_id, Transaction.book_id == book_id)
        )
        result = session.exec(transaction_query)

        transaction = result.one_or_none()
        if transaction is None:
            return None

        return transaction
    except Exception as e:
        logger.error(f"Error finding transaction: {e}")
        raise


def update_transaction_status(
    user_id: str, status: TransactionStatus, session: Session
):
    try:
        transaction_query = select(Transaction).where(Transaction.user_id == user_id)
        result = session.exec(transaction_query)

        transaction = result.one_or_none()

        transaction.status = status
        transaction.updated_at = datetime.now(timezone.utc)

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return transaction
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating transaction status: {e}")
        raise


def list_my_transaction(user_id: str, offset: int, limit: int, session: Session):
    try:
        transaction_query = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .offset((offset - 1) * limit)
            .limit(limit)
        )
        result = session.exec(transaction_query)

        transactions = result.fetchall()
        transaction_count = session.scalar(
            select(func.count()).select_from(Transaction)
        )

        return {
            "transactions": jsonable_encoder(transactions),
            "total_count": transaction_count,
            "offset": offset,
            "limit": limit,
            "offset_total": math.ceil(transaction_count / limit),
        }
    except Exception as e:
        logger.error(f"Error listing transaction: {e}")
        raise


def list(offset: int, limit: int, session: Session):
    try:
        transaction_query = (
            select(Transaction).offset((offset - 1) * limit).limit(limit)
        )
        result = session.exec(transaction_query)

        transactions = result.fetchall()
        transaction_count = session.scalar(
            select(func.count()).select_from(Transaction)
        )

        return {
            "transactions": jsonable_encoder(transactions),
            "total_count": transaction_count,
            "offset": offset,
            "limit": limit,
            "offset_total": math.ceil(transaction_count / limit),
        }
    except Exception as e:
        logger.error(f"Error listing transaction: {e}")
        raise
