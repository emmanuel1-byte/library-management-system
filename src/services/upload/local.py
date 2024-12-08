from ...helpers.upload import FileValidator
from fastapi import UploadFile
from fastapi import HTTPException
import os
from ...utils.logger import logger


async def upload_file_to_memory(file: UploadFile, upload_dir: str):
    try:
        await FileValidator().validate_file(file)
        os.makedirs(upload_dir, exist_ok=True)

        file.file.seek(0)
        file_path = os.path.join(upload_dir, file.filename)

        file_content = await file.read()
        if not file_content:
            raise HTTPException(
                status_code=400, detail={"message": "File content is empty."}
            )

        with open(file_path, "wb") as f:
            f.write(file_content)
        logger.info(f"Saved successfully: {file_path}")

    except Exception as e:
        if hasattr(e, "status_code") and hasattr(e, "detail"):
            logger.error(f"Custom error: {e}")
            raise HTTPException(status_code=e.status_code, detail={"message": e.detail})

        logger.error(f"Unexpected error during upload: {e}")
        raise HTTPException(
            status_code=500,
            detail={"message": "File upload failed due to an unexpected error."},
        )
