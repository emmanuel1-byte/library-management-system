from src import User
from src import Profile
from sqlmodel import Session, select
from .schema import Signup_schema
from ...utils.logger import logger
import bcrypt
from datetime import datetime, timezone


def create_user(data: Signup_schema, session: Session):
    try:
        data.password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt(rounds=12)
        ).decode("utf-8")
        new_user = User(**data.model_dump())

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        new_profile = Profile(user_id=new_user.id)
        session.add(new_profile)
        session.commit()

        return new_user
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating new user: {e}")
        raise 


def get_user_by_email(email: str, session: Session):
    try:
        user_query = select(User).where(User.email == email)
        result = session.exec(user_query).one_or_none()

        if result is None:
            return None
        return result

    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise 


def get_user_by_id(id: str, session: Session):
    try:
        user_query = select(User).where(User.id == id)
        result = session.exec(user_query).one_or_none()

        if result is None:
            return None
        return result
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise 


def update_verification_status(user_id: str, session: Session):
    try:
        user_query = select(User).where(User.id == user_id)
        result = session.exec(user_query)
        user = result.one_or_none()

        if result is None:
            return None

        user.verified = True
        user.updated_at = datetime.now(timezone.utc)

        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating verifcation status: {e}")
        raise 


def update_password(user_id: str, password: str, session: Session):
    try:
        user_query = select(User).where(User.id == user_id)
        result = session.exec(user_query)
        user = result.one_or_none()

        if user is None:
            return None

        user.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt(rounds=12)
        ).decode("utf-8")
        user.updated_at = datetime.now(timezone.utc)

        session.add(user)
        session.commit()
        session.refresh(user)

    except Exception as e:
        session.rollback()
        logger.error(f"Error updating password: {e}")
        raise 
