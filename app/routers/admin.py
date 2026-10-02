from pathlib import Path
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from app import models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("/users", response_model=schemas.PaginatedUsersResponse)
def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
    current_admin: models.User = Depends(deps.get_current_admin)
):
    query = db.query(models.User)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                models.User.fullName.ilike(search_filter),
                models.User.email.ilike(search_filter)
            )
        )
    
    total = query.count()
    total_pages = (total + limit - 1) // limit
    
    users = query.offset((page - 1) * limit).limit(limit).all()
    
    return schemas.PaginatedUsersResponse(
        users=users,
        total=total,
        page=page,
        totalPages=total_pages
    )

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user_status(
    user_id: str,
    update_data: schemas.UserAdminUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: models.User = Depends(deps.get_current_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    user.paymentStatus = update_data.paymentStatus
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_admin: models.User = Depends(deps.get_current_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    db.delete(user)
    db.commit()
    return None

@router.get("/submissions", response_model=List[schemas.SubmissionResponse])
def get_all_submissions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[models.SubmissionStatusEnum] = Query(None, alias="status"),
    db: Session = Depends(deps.get_db),
    current_admin: models.User = Depends(deps.get_current_admin)
):
    query = db.query(models.PaperSubmission).options(
        joinedload(models.PaperSubmission.user)
    )
    
    if status_filter:
        query = query.filter(models.PaperSubmission.status == status_filter)
        
    submissions = query.offset((page - 1) * limit).limit(limit).all()
    return submissions

@router.get("/submissions/{submission_id}/download")
def download_submission(
    submission_id: UUID,
    db: Session = Depends(deps.get_db),
    current_admin: models.User = Depends(deps.get_current_admin)
):
    submission = db.query(models.PaperSubmission).filter(
        models.PaperSubmission.id == submission_id
    ).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")

    upload_root = Path(settings.UPLOAD_DIR).resolve()
    file_path = Path(submission.filePath).resolve()
    try:
        file_path.relative_to(upload_root)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission file not found")

    if not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission file not found")

    filename = Path(submission.originalFileName.replace("\\", "/")).name
    if not filename:
        filename = f"{submission.id}.pdf"

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename,
    )

from pydantic import BaseModel
class AdminSubmissionUpdate(BaseModel):
    status: models.SubmissionStatusEnum

@router.put("/submissions/{submission_id}", response_model=schemas.SubmissionResponse)
def update_submission_status(
    submission_id: str,
    update_data: AdminSubmissionUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: models.User = Depends(deps.get_current_admin)
):
    submission = db.query(models.PaperSubmission).filter(models.PaperSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
        
    submission.status = update_data.status
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    return submission

@router.get("/stats", response_model=schemas.AdminStatsResponse)
def get_system_stats(
    db: Session = Depends(deps.get_db),
    current_admin: models.User = Depends(deps.get_current_admin)
):
    total_registrations = db.query(models.User).count()
    payments_completed = db.query(models.User).filter(models.User.paymentStatus == models.PaymentStatusEnum.COMPLETED).count()
    pending_payments = db.query(models.User).filter(models.User.paymentStatus == models.PaymentStatusEnum.PENDING).count()
    total_submissions = db.query(models.PaperSubmission).count()
    
    return schemas.AdminStatsResponse(
        totalRegistrations=total_registrations,
        paymentsCompleted=payments_completed,
        totalSubmissions=total_submissions,
        pendingPayments=pending_payments
    )
