from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from .schema import User_Schema, Update_User_Schema
from typing import Annotated
from ...helpers.authorize_role import RoleChecker
from sqlmodel import Session
from ...utils.database import get_session
from ...helpers.authenticate_user import get_current_user
from . import repository

user = APIRouter(prefix="/api/users")


@user.post("/", tags=["User"])
def create_user(
    validated_data: User_Schema,
    session: Annotated[Session, Depends(get_session)],
    user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
):
    existing_user = repository.get_user_by_email(validated_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=409, detail={"message": "Account already exist"}
        )

    new_user = repository.create(validated_data, session)

    return JSONResponse(
        content={
            "data": {"user": new_user.model_dump(mode="json", exclude="password")}
        },
        status_code=201,
    )


@user.get("/", tags=["User"])
def list_users(
    session: Annotated[Session, Depends(get_session)],
    user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
    offset: int = 1,
    limit: int = 10,
):
    data = repository.list(offset, limit, session)
    return JSONResponse(content={"data": data})


@user.put("/{user_id}", tags=["User"])
def update_user(
    validated_data: Update_User_Schema,
    user_id: str,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
):
    user = repository.update(validated_data, user_id, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    return JSONResponse(
        content={"data": {"user": user.model_dump(mode="json", exclude="password")}}
    )


@user.delete("/{user_id}", tags=["User"])
def update_user(
    user_id: str,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin"])),
):

    user = repository.delete(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    return JSONResponse(content={"message": "Account deleted"})
