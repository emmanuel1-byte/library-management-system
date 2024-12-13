from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Annotated
from ...utils.database import get_session
from ...helpers.authenticate_user import get_current_user
from ...helpers.authorize_role import RoleChecker
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from . import repository
from .schema import Transaction_Schema

transaction = APIRouter(prefix="/api/transactions")


@transaction.post("/borrow", tags=["Transaction"])
def borrow_book(
    validated_data: Transaction_Schema,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Member"])),
):
    book = repository.find_book_by_id(validated_data.book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail={"message": "Book does not exist"})

    if book.get("available_copies") <= 0:
        raise HTTPException(status_code=400, detail={"message": "Book not available"})

    existing_transaction = repository.find_transaction(
        current_user_id, book.get("id"), session
    )

    if existing_transaction:
        raise HTTPException(
            status_code=409, detail={"message": "You have borrowed this book already"}
        )

    repository.create_transaction(current_user_id, validated_data.book_id, session)
    repository.update_available_copies(validated_data.book_id, False, session)

    return JSONResponse(
        content={"message": "Book borrowed"},
        status_code=200,
    )


@transaction.patch("/return", tags=["Transaction"])
def return_book(
    validated_data: Transaction_Schema,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Member"])),
):
    book = repository.find_book_by_id(validated_data.book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail={"message": "Book does not exist"})

    repository.update_available_copies(book.get("id"), True, session)
    repository.update_transaction_status(current_user_id, "Returned", session)

    return JSONResponse(content={"message": "Book returned"}, status_code=200)


@transaction.get("/me", tags=["Transaction"])
def list_transactions(
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Member"])),
    offset: int = 1,
    limit: int = 10,
):

    transactions = repository.list_my_transaction(
        current_user_id, offset, limit, session
    )
    return JSONResponse(content={"data": transactions}, status_code=200)


@transaction.get("/", tags=["Transaction"])
def list_transactions(
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
    offset: int = 1,
    limit: int = 10,
):

    transactions = repository.list(offset, limit, session)
    return JSONResponse(content={"data": transactions}, status_code=200)
