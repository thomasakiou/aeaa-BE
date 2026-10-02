from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app import models, schemas
from app.api import deps
from app.services.email import send_contact_email

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.ContactResponse)
def submit_contact(contact_in: schemas.ContactCreate, db: Session = Depends(deps.get_db)):
    contact_msg = models.ContactMessage(
        senderName=contact_in.name,
        senderEmail=contact_in.email,
        subject=contact_in.subject,
        message=contact_in.message
    )
    db.add(contact_msg)
    
    try:
        send_contact_email(
            name=contact_in.name,
            email=contact_in.email,
            subject=contact_in.subject,
            message=contact_in.message
        )
    except Exception as e:
        logger.exception("Failed to send contact email")
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Your message was saved, but email delivery failed. Please try again later.",
        ) from e
    
    db.commit()
    db.refresh(contact_msg)
    
    return schemas.ContactResponse(message="Your message has been sent successfully.")
