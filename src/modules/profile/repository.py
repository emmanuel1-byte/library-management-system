from .schema import Profile_Schema
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
from .model import Profile
from src import User


def update_profile(data: Profile_Schema, user_id: str, session: Session):
    try:
        profile_query = (
            select(Profile, User).join(User).where(Profile.user_id == user_id)
        )
        result = session.exec(profile_query).one_or_none()
        if result is None:
            return None

        profile, user = result

        profile.bio = data.bio
        user.fullname = data.fullname
        user.email = data.email

        session.add(profile)
        session.add(user)
        session.commit()
        session.refresh(profile)
        session.refresh(user)

        return {
            "profile": jsonable_encoder(profile, exclude=["created_at", "updated_at"]),
            "user": jsonable_encoder(
                user,
                exclude=["password", "roles", "verified", "created_at", "updated_at"],
            ),
        }

    except Exception as e:
        session.rollback()
        raise (e)


def update_profile_picture(user_id: str, file_url: str, session: Session):
    try:
        profile_query = (
            select(Profile, User).join(User).where(Profile.user_id == user_id)
        )
        result = session.exec(profile_query).one_or_none()
        if result is None:
            return None

        profile, user = result

        profile.profile_picture = file_url

        session.add(profile)
        session.commit()
        session.refresh(profile)
        session.refresh(user)

        return {
            "profile": jsonable_encoder(profile, exclude=["created_at", "updated_at"]),
            "user": jsonable_encoder(
                user,
                exclude=["password", "roles", "verified", "created_at", "updated_at"],
            ),
        }

    except Exception as e:
        session.rollback()
        raise (e)


def update_cover_picture(user_id: str, file_url: str, session: Session):
    try:
        profile_query = (
            select(Profile, User).join(User).where(Profile.user_id == user_id)
        )
        result = session.exec(profile_query).one_or_none()
        if result is None:
            return None

        profile, user = result

        profile.cover_picture = file_url

        session.add(profile)
        session.commit()
        session.refresh(profile)
        session.refresh(user)

        return {
            "profile": jsonable_encoder(profile, exclude=["created_at", "updated_at"]),
            "user": jsonable_encoder(
                user,
                exclude=["password", "roles", "verified", "created_at", "updated_at"],
            ),
        }

    except Exception as e:
        session.rollback()
        raise (e)


def get_profile(user_id: str, session: Session):
    try:
        profile_query = (
            select(Profile, User).join(User).where(Profile.user_id == user_id)
        )
        result = session.exec(profile_query).one_or_none()
        if result is None:
            return None

        profile, user = result

        return {
            "profile": jsonable_encoder(profile, exclude=["created_at", "updated_at"]),
            "user": jsonable_encoder(
                user,
                exclude=["password", "roles", "verified", "created_at", "updated_at"],
            ),
        }
    except Exception as e:
        session.rollback()
        raise e
