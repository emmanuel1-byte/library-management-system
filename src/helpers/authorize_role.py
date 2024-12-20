from typing import Annotated, List
from src import User
from ..utils.database import get_session
from sqlmodel import select, Session
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from .authenticate_user import get_current_user
from ..utils.logger import logger


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
        session: Annotated[Session, Depends(get_session)],
    ):
        try:
            user = session.exec(select(User).where(User.id == user_id)).one_or_none()
            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail={"message": "Account does not exist"},
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not any(role in self.allowed_roles for role in user.roles):
                raise HTTPException(
                    status_code=403,
                    detail={"message": "Unauthorized access"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return True
        except Exception as e:
            logger.error(f"Role Check failed: {e}")
            raise 
