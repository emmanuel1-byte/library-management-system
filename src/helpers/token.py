import jwt
from fastapi import HTTPException
from ..utils.logger import logger
from jwt import InvalidTokenError, ExpiredSignatureError
import dotenv
from datetime import datetime, timezone, timedelta

dotenv.load_dotenv()
import os


def decode_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms="HS256")
        return payload.get("sub")

    except InvalidTokenError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail={"message": "Invalid token"})

    except ExpiredSignatureError as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail={"message": "Token has expired!"})


def create_verification_token(user_id: str):
    token = jwt.encode(
        {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=60)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token


def create_access_token(user_id: str):
    token = jwt.encode(
        {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=60)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token


def create_refresh_token(user_id: str):
    token = jwt.encode(
        {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=60)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token


def create_reset_password_token(user_id: str):
    token = jwt.encode(
        {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=60)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token
