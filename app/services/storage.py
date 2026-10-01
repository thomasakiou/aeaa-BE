import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException
from app.core.config import settings

def save_upload_file(file: UploadFile) -> tuple[str, float]:
    """
    Saves an uploaded file to the local disk.
    Returns a tuple of (file_path, file_size_mb).
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Force .pdf extension based on the router check
    file_extension = ".pdf"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)

    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        os.remove(file_path)
        raise HTTPException(
            status_code=400, 
            detail=f"File too large. Max size is {settings.MAX_FILE_SIZE_MB}MB"
        )
        
    return file_path, file_size_mb
