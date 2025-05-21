from fastapi import UploadFile, HTTPException
from typing import Dict, Any
import base64
from app.core.config import settings
from app.services.interfaces import FileHandler


class ImageFileHandler(FileHandler):
    async def validate_file(self, file: UploadFile) -> bool:
        """Validate image file type and size."""
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, detail=f"File type {file.content_type} not allowed"
            )

        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size too large")
        await file.seek(0)
        return True

    async def process_file(self, file: UploadFile) -> Dict[str, Any]:
        """Convert image to base64 and prepare for GPT."""
        if not file.content_type.startswith("image/"):
            return None

        contents = await file.read()
        await file.seek(0)
        base64_image = base64.b64encode(contents).decode("utf-8")

        return {"type": "image", "image": base64_image, "source": file.filename}
