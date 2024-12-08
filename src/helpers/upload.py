from fastapi import UploadFile, HTTPException
from typing import Dict, Set, Optional
import magic
import os


class FileValidator:
    DEFAULT_MAX_SIZE: int = 2 * 1024 * 1024  # 2mb
    ALLOWED_MIME_TYPES: Dict[str, Set[str]] = {
        "image": {"image/jpeg", "image/png", "image/webp"},
        # "document": {
        #     "application/pdf",
        #     "application/msword",
        #     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        #     "application/vnd.ms-excel",
        #     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        # },
        # "video": {"video/mp4", "video/mpeg", "video/webm"},
    }

    def __init__(
        self,
        max_file: Optional[int] = None,
        allowed_mime_types: Optional[Set[str]] = None,
    ):
        self.max_file = max_file or self.DEFAULT_MAX_SIZE
        self.allowed_types = allowed_mime_types or self.ALLOWED_MIME_TYPES

    async def validate_file(self, file: UploadFile):
        file_content = await file.read()
        file_size = len(file_content)

        # Get the mimeType from magic by reading some bytes from the fil
        mime_type = magic.from_buffer(file_content[:8192], mime=True)

        if self.allowed_types:
            mime_category = self._get_mime_category(mime_type)
            if (
                not mime_category
                or mime_type not in self.ALLOWED_MIME_TYPES[mime_category]
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {mime_type.split("/")[1]} is not allowed",
                )

        if file_size > self.max_file:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"File size exceeds maximum limit of {self.max_file/ (1024*1024):.1f}MB"
                },
            )

        return True

    def _get_mime_category(self, mime_type: str):
        for category, mime_types in self.ALLOWED_MIME_TYPES.items():
            if mime_type in mime_types:
                return category
        return None
