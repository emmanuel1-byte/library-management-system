import cloudinary
import dotenv

dotenv.load_dotenv()
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET_KEY"),
)
from cloudinary import uploader
from fastapi import UploadFile, HTTPException
from ...helpers.upload import FileValidator
from ...utils.logger import logger


async def upload_to_cloudinary(file: UploadFile):
    try:
        await FileValidator().validate_file(file)
        file.file.seek(0)

        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400, detail={"message": "File content is empty."}
            )

        # Upload the file content to Cloudinary
        uploaded_file = uploader.upload(file_content, resource_type="image")

        return uploaded_file.get("url")

    except Exception as e:
        if hasattr(e, "status_code") and hasattr(e, "detail"):
            logger.error(f"Custom error: {e}")
            raise HTTPException(status_code=e.status_code, detail={"message": e.detail})

        logger.error(f"Unexpected error during upload: {e}")
        raise HTTPException(
            status_code=500,
            detail={"message": "File upload failed due to an unexpected error."},
        )
