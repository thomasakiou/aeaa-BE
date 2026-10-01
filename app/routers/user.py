import os
import uuid
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("/profile", response_model=schemas.UserResponse)
def get_profile(current_user: models.User = Depends(deps.get_current_user)):
    return current_user

@router.put("/profile", response_model=schemas.UserResponse)
def update_profile(
    user_in: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    if user_in.fullName is not None:
        current_user.fullName = user_in.fullName
    if user_in.organization is not None:
        current_user.organization = user_in.organization
    if user_in.country is not None:
        current_user.country = user_in.country
    if user_in.phoneNumber is not None:
        current_user.phoneNumber = user_in.phoneNumber

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/submissions", response_model=List[schemas.SubmissionResponse])
def get_user_submissions(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    return db.query(models.PaperSubmission).filter(
        models.PaperSubmission.userId == current_user.id
    ).all()

@router.post("/submissions", response_model=schemas.SubmissionResponse, status_code=status.HTTP_201_CREATED)
def upload_submission(
    title: str = Form(...),
    subTheme: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    from app.services.storage import save_upload_file
    file_path, file_size_mb = save_upload_file(file)

    submission = models.PaperSubmission(
        userId=current_user.id,
        title=title,
        subTheme=subTheme,
        filePath=file_path,
        originalFileName=file.filename,
        fileSizeMB=file_size_mb
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission
