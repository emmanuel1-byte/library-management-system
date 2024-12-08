from fastapi import HTTPException, Depends
from src import User
from sqlmodel import Session, select
from ..utils.database import get_session
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt
import dotenv

dotenv.load_dotenv()
import os

security = HTTPBearer()


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session)],
):

    try:
        payload = jwt.decode(
            token.credentials, os.getenv("JWT_SECRET"), algorithms="HS256"
        )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail={"message": "Could not validate credentials"},
            )

    except InvalidTokenError:
        raise HTTPException(status_code=400, detail={"message": "Invalid token"})

    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail={"message": "Token has expired!"})

    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(
            status_code=403,
            detail={"message": "Account associated with this token does not exist"},
        )
    return user.id
