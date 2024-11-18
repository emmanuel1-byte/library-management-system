from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session
from fastapi.responses import JSONResponse
from .schema import (
    Signup_schema,
    Resend_email_Schema,
    Login_Schema,
    Forgot_Password_Schema,
    Reset_Password_Schema,
)
from ...utils.database import get_session
from . import repository
from ...utils.email import send_verification_email, send_reset_password_email
from ...helpers.token import (
    create_verification_token,
    create_access_token,
    create_refresh_token,
    create_reset_password_token,
    decode_token,
)
from ...helpers.authenticate_user import get_current_user
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import BackgroundTasks
import bcrypt

auth = APIRouter(prefix="/api/auth")


@auth.post("/signup", tags=["Authentication"])
def signup(
    validated_data: Signup_schema,
    session: Annotated[Session, Depends(get_session)],
    background_tasks: BackgroundTasks,
):
    existing_user = repository.get_user_by_email(validated_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=409, detail={"message": "Account already exist"}
        )

    new_user = repository.create_user(validated_data, session)
    if new_user:
        verification_token = create_verification_token(new_user.id)
        background_tasks.add_task(
            send_verification_email, new_user.email, verification_token
        )

    return JSONResponse(
        content={
            "message": "Account created",
            "data": {"user": new_user.model_dump(mode="json", exclude="password")},
        },
        status_code=201,
    )


@auth.get("/verify-email", tags=["Authentication"])
def verify_email(token: str, session: Annotated[Session, Depends(get_session)]):
    user_id = decode_token(token)

    user = repository.get_user_by_id(user_id, session)
    if user is None:
        return HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    repository.update_verification_status(user.id, session)

    return JSONResponse(content={"message": "Account verified"}, status_code=200)


@auth.post("/resend-verification-email", tags=["Authentication"])
def resend_verification_email(
    validated_schema: Resend_email_Schema,
    session: Annotated[Session, Depends(get_session)],
    background_tasks: BackgroundTasks,
):
    user = repository.get_user_by_email(validated_schema.email, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    if user.verified:
        raise HTTPException(
            status_code=409, detail={"message": "Account already verified"}
        )

    verification_token = create_verification_token(user.id)
    background_tasks.add_task(send_verification_email, user.email, verification_token)

    return JSONResponse(
        content={"message": "Email sent check your inbox"}, status_code=200
    )


@auth.post("/login", tags=["Authentication"])
def login(
    validated_data: Login_Schema, session: Annotated[Session, Depends(get_session)]
):
    user = repository.get_user_by_email(validated_data.email, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    if not user.verified:
        raise HTTPException(
            status_code=401,
            detail={"message": "Verify your email address to continue."},
        )

    compare_password = bcrypt.checkpw(
        validated_data.password.encode("utf-8"), user.password.encode("utf-8")
    )

    if not compare_password:
        raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return JSONResponse(
        content={
            "data": {
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            }
        }
    )


@auth.post("/forgot-password", tags=["Authentication"])
def forgot_password(
    valdated_data: Forgot_Password_Schema,
    session: Annotated[Session, Depends(get_session)],
    background_tasks: BackgroundTasks,
):
    user = repository.get_user_by_email(valdated_data.email, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    reset_password_token = create_reset_password_token(user.id)
    background_tasks.add_task(
        send_reset_password_email, user.email, reset_password_token
    )

    return JSONResponse(
        content={"message": "Reset password email sent check your inbox"}
    )


@auth.get("/reset-password/{token}", tags=["Authentication"])
def verify_reset_password_token(
    token: str, session: Annotated[Session, Depends(get_session)]
):
    user_id = decode_token(token)

    user = repository.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    return JSONResponse(content={"message": "Token is valid"})


@auth.patch("/reset-password", tags=["Authentication"])
def reset_password(
    validated_data: Reset_Password_Schema,
    session: Annotated[Session, Depends(get_session)],
):
    user_id = decode_token(validated_data.token)

    user = repository.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    repository.update_password(user.id, validated_data.password, session)

    return JSONResponse(content={"message": "Password updated"})


@auth.post("/refresh-token", tags=["Authentication"])
def refresh_token(
    session: Annotated[Session, Depends(get_session)],
    user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
):
    user = repository.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return JSONResponse(
        content={
            "data": {
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            }
        }
    )
