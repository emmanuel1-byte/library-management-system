import dotenv
import magic
import os
from ...utils.logger import logger
from fastapi import UploadFile, HTTPException
from ...helpers.upload import FileValidator

dotenv.load_dotenv()
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")


async def upload_file_to_s3(file: UploadFile):
    try:
        await FileValidator().validate_file(file)

        file.file.seek(0)
        contentType = magic.from_buffer(await file.read(), mime=True)
        file.file.seek(0)

        response = s3.put_object(
            Bucket=os.getenv("AWS_S3_BUCKET_NAME"),
            Key=file.filename,
            Body=file.file.read(),
            ContentType=contentType,
        )

        if response is None:
            raise HTTPException(
                status_code=500,
                detail={"message": "File upload failed due to an unexpected error."},
            )

        uploaded_file = f"https://{os.getenv('AWS_S3_BUCKET_NAME')}.s3.amazonaws.com/{file.filename}"
        return uploaded_file
    except ClientError as e:
        logger.error(f"Unexpected error during upload: {e}")
        raise e

    except Exception as e:
        if hasattr(e, "status_code") and hasattr(e, "detail"):
            logger.error(f"Custom error: {e}")
            raise HTTPException(status_code=e.status_code, detail={"message": e.detail})
        logger.error(f"Unexpected error during upload: {e}")

        raise HTTPException(
            status_code=500,
            detail={"message": "File upload failed due to an unexpected error."},
        )
