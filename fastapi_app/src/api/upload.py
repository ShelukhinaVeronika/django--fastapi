import os
import shutil

from datetime import datetime
from fastapi import UploadFile, HTTPException
from pathlib import Path

UPLOAD_DIR = "uploads/posts"

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def save_image(file: UploadFile, user_id: int) -> str:

    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, detail="Invalid image type. Allowed: JPEG, PNG, GIF, WEBP"
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{user_id}_{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/{UPLOAD_DIR}/{filename}"


def delete_image(image_path: str):
    if image_path:
        full_path = image_path.lstrip("/")
        if os.path.exists(full_path):
            os.remove(full_path)
