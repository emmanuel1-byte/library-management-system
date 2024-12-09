from .schema import Book_Schema
from sqlmodel import Session, select, func
from .model import Book
from fastapi.encoders import jsonable_encoder
import math


def add_book(data: Book_Schema, session: Session):
    try:
        new_book = Book(**data.model_dump())

        session.add(new_book)
        session.commit()
        session.refresh(new_book)

        return new_book
    except Exception as e:
        session.rollback()
        raise e


def find_book_by_title(title: str, session: Session):
    try:
        book__query = select(Book).where(Book.title == title)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        return book
    except Exception as e:
        session.rollback()
        raise e


def find_book_by_id(book_id: str, session: Session):
    try:
        book__query = select(Book).where(Book.id == book_id)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        return jsonable_encoder(book)
    except Exception as e:
        session.rollback()
        raise e


def list(offset: int, limit: int, session: Session):
    try:
        book_query = select(Book).offset((offset - 1) * limit).limit(limit)
        result = session.exec(book_query)

        books = result.fetchall()
        user_count = session.scalar(select(func.count()).select_from(Book))

        return {
            "user": jsonable_encoder(books, exclude=["password"]),
            "total_count": user_count,
            "offset": offset,
            "limit": limit,
            "offset_total": math.ceil(user_count / limit),
        }
    except Exception as e:
        session.rollback()
        raise e


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

        session.add(book)
        session.commit()
        session.refresh(book)

        return jsonable_encoder(book)
    except Exception as e:
        session.rollback()
        raise e


def update_file_url(book_id: str, file_url: str, session: Session):
    try:
        book__query = select(Book).where(Book.id == book_id)
        result = session.exec(book__query)

        book = result.one_or_none()

        if book is None:
            return None

        book.file_url = file_url

        session.add(book)
        session.commit()
        session.refresh(book)

        return jsonable_encoder(book)
    except Exception as e:
        session.rollback()
        raise e


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
        raise e
