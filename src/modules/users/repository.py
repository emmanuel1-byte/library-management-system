from sqlmodel import Session, select
from fastapi.encoders import jsonable_encoder
from ...utils.logger import logger
from .schema import User_Schema
from .model import User
import bcrypt
from sqlalchemy import func
import math


def create(data: User_Schema, session: Session):
    try:
        data.password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt(rounds=12)
        ).decode("utf-8")

        new_user = User(**data.model_dump())
        new_user.verified = True

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating user: {e}")
        raise e


def list(offset: int, limit: int, session: Session):
    try:
        statement = select(User).offset((offset - 1) * limit).limit(limit)
        result = session.exec(statement)

        users = result.fetchall()
        user_count = session.scalar(select(func.count()).select_from(User))

        return {
            "user": jsonable_encoder(users, exclude=["password"]),
            "total_count": user_count,
            "offset": offset,
            "limit": limit,
            "offset_total": math.ceil(user_count / limit),
        }
    except Exception as e:
        session.rollback()
        logger.error(f"Error retrieving list of users: {e}")
        raise e


def update(data: User_Schema, user_id: str, session: Session):
    try:
        statement = select(User).where(User.id == user_id)
        result = session.exec(statement)
        user = result.first()

        if user is None:
            return None

        user.fullname = data.fullname
        user.email = data.email
        user.password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt(rounds=12)
        ).decode("utf-8")

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating user: {e}")
        raise e


def delete(user_id: str, session: Session):
    try:
        statement = select(User).where(User.id == user_id)
        result = session.exec(statement)

        user = result.first()
        if user is None:
            return None

        session.delete(user)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting user: {e}")
        raise e


def get_user_by_email(email: str, session: Session):
    try:
        statement = select(User).where(User.email == email)
        result = session.exec(statement)

        user = result.first()
        if user is None:
            return None
        return user

    except Exception as e:
        session.rollback()
        logger.error(f"Error fetching user: {e}")
        raise e
