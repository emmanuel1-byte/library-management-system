from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session
from .schema import Book_Schema
from typing import Annotated
from ...utils.database import get_session
from ...helpers.authenticate_user import get_current_user
from ...helpers.authorize_role import RoleChecker
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from ...services.upload.cloudinary import upload_to_cloudinary
from . import repository


book = APIRouter(prefix="/api/books")


@book.post("/", tags=["Book"])
def add_new_book(
    validated_data: Book_Schema,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
):
    existing_book = repository.find_book_by_title(validated_data.title, session)
    if existing_book:
        raise HTTPException(status_code=409, detail={"message": "Book already exist"})

    new_book = repository.add_book(validated_data, session)
    return JSONResponse(
        content={"data": {"book": new_book.model_dump(mode="json")}}, status_code=201
    )


@book.get("/{book_id}", tags=["Book"])
def get_book_by_id(
    book_id: str,
    session: Annotated[Session, Depends(get_session)],
):
    book = repository.find_book_by_id(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail={"message": "Book does not exist"})

    return JSONResponse(content={"data": book}, status_code=201)


@book.get("/", tags=["Book"])
def list_books(
    session: Annotated[Session, Depends(get_session)],
    offset: int = 1,
    limit: int = 10,
):
    books = repository.list(offset, limit, session)
    return JSONResponse(content={"data": books}, status_code=201)


@book.patch("/upload/file/{book_id}", tags=["Book"])
async def upload_file(
    file: UploadFile,
    book_id: str,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
):

    if not file:
        raise HTTPException(status_code=400, detail="Attach a file")

    uploaded_file = await upload_to_cloudinary(file)
    book = repository.update_file_url(book_id, uploaded_file, session)
    if book is None:
        raise HTTPException(status_code=404, detail={"message": "Book does not exist"})

    return JSONResponse(content={"data": book}, status_code=200)


@book.put("/{book_id}", tags=["Book"])
def update_book_by_id(
    book_id: str,
    validated_data: Book_Schema,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
):
    book = repository.update_book(validated_data, book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail={"message": "Book does not exist"})

    return JSONResponse(content={"data": book}, status_code=200)


@book.delete("/{book_id}", tags=["Book"])
def delete_book_by_id(
    book_id: str,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
):
    book = repository.delete_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail={"message": "Book does not exist"})

    return JSONResponse(content={"message": "Book deleted"}, status_code=200)
