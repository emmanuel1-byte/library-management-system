from .schema import Book_Schema
from sqlmodel import Session, select, func
from .model import Book
from fastapi.encoders import jsonable_encoder
import math
from sqlalchemy import cast, String
from datetime import datetime, timezone
from ...utils.logger import logger


def add_book(data: Book_Schema, session: Session):
    try:
        new_book = Book(**data.model_dump())

        session.add(new_book)
        session.commit()
        session.refresh(new_book)

        return new_book
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding book: {e}")
        raise


def find_book_by_title(title: str, session: Session):
    try:
        book__query = select(Book).where(Book.title == title)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        return book
    except Exception as e:
        logger.error(f"Error finding book by title: {e}")
        raise


def find_book_by_id(book_id: str, session: Session):
    try:
        book__query = select(Book).where(Book.id == book_id)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        return jsonable_encoder(book)
    except Exception as e:
        logger.error(f"Error finding book by ID: {e}")
        raise


def list(offset: int, limit: int, query: str, session: Session):
    try:
        if query:
            book_query = (
                select(Book)
                .where(
                    (cast(Book.title, String).ilike(f"%{query}%"))
                    | (cast(Book.author, String).ilike(f"%{query}%"))
                    | (cast(Book.genre, String).ilike(f"%{query}%"))
                )
                .offset((offset - 1) * limit)
                .limit(limit)
            )
            total_count_query = select(func.count()).where(
                (cast(Book.title, String).ilike(f"%{query}%"))
                | (cast(Book.author, String).ilike(f"%{query}%"))
                | (cast(Book.genre, String).ilike(f"%{query}%"))
            )
        else:
            book_query = select(Book).offset((offset - 1) * limit).limit(limit)
            total_count_query = select(func.count()).select_from(Book)

        result = session.exec(book_query)
        books = result.fetchall()

        user_count = session.scalar(total_count_query)

        return {
            "books": jsonable_encoder(books),
            "total_count": user_count,
            "offset": offset,
            "limit": limit,
            "offset_total": math.ceil(user_count / limit),
        }

    except Exception as e:
        logger.error(f"Error listing book: {e}")
        raise


def update_book(data: Book_Schema, book_id: str, session: Session):
    try:
        book__query = select(Book).where(Book.id == book_id)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        book.author = data.author
        book.title = data.title
        book.genre = data.genre
        book.isbn = data.isbn
        book.available_copies = data.available_copies
        book.total_copies = data.total_copies

        book.updated_at = datetime.now(timezone.utc)

        session.add(book)
        session.commit()
        session.refresh(book)

        return jsonable_encoder(book)
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating book: {e}")
        raise


def update_file_url(book_id: str, file_url: str, session: Session):
    try:
        book__query = select(Book).where(Book.id == book_id)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        book.file_url = file_url
        book.updated_at = datetime.now(timezone.utc)

        session.add(book)
        session.commit()
        session.refresh(book)

        return jsonable_encoder(book)
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating book file: {e}")
        raise


def delete_book(book_id: str, session: Session):
    try:
        book__query = select(Book).where(Book.id == book_id)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        session.delete(book)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting book: {e}")
        raise
