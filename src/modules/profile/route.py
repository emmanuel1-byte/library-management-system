from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from ...services.upload.cloudinary import upload_to_cloudinary
from . import repository
from .schema import Profile_Schema
from typing import Annotated
from sqlmodel import Session
from fastapi.security.http import HTTPAuthorizationCredentials
from ...utils.database import get_session
from ...helpers.authenticate_user import get_current_user
from ...helpers.authorize_role import RoleChecker
from ...helpers.upload import UploadFile

profile = APIRouter(prefix="/api/profile")


@profile.get("/me", tags=["Profile"])
def get_profile(
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin", "Member"])),
):
    profile = repository.get_profile(current_user_id, session)
    if profile is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    return JSONResponse(content={"data": profile}, status_code=200)


@profile.put("/me", tags=["Profile"])
def update_profile(
    validated_data: Profile_Schema,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin", "Member"])),
):
    profile = repository.update_profile(validated_data, current_user_id, session)
    if profile is None:
        raise HTTPException(
            status_code=404, detail={"message": "Profile does not exist"}
        )

    return JSONResponse(content={"data": profile}, status_code=200)


@profile.patch("/upload/profile_picture", tags=["Profile"])
async def upload_profile_picture(
    file: UploadFile,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin", "Member"])),
):
    if not file:
        raise HTTPException(status_code=400, detail="Attach a file")

    uploaded_profile_picture_url = await upload_to_cloudinary(file)
    profile = repository.update_profile_picture(
        current_user_id, uploaded_profile_picture_url, session
    )

    if profile is None:
        raise HTTPException(
            status_code=404, detail={"message": "Profile does not exist"}
        )
    return JSONResponse(content={"data": profile}, status_code=200)


@profile.patch("/upload/cover_picture", tags=["Profile"])
async def upload_cover_picture(
    file: UploadFile,
    session: Annotated[Session, Depends(get_session)],
    current_user_id: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    authorized: bool = Depends(RoleChecker(["Admin", "Member"])),
):
    if not file:
        raise HTTPException(status_code=400, detail="Attach a file")

    uploaded_cover_picture_url = await upload_to_cloudinary(file)
    profile = repository.update_cover_picture(
        current_user_id, uploaded_cover_picture_url, session
    )
    if profile is None:
        raise HTTPException(
            status_code=404, detail={"message": "Profile does not exist"}
        )
    return JSONResponse(content={"data": profile}, status_code=200)
