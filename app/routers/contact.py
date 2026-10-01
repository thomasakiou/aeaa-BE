from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.services.email import send_contact_email

router = APIRouter()

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
        print(f"Failed to send email: {e}")
    
    db.commit()
    db.refresh(contact_msg)
    
    return schemas.ContactResponse(message="Your message has been sent successfully.")
