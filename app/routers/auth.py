from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.core import security

router = APIRouter()

@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system.",
        )
    
    if user_in.password != user_in.confirmPassword:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match.",
        )
    
    user = models.User(
        fullName=user_in.fullName,
        email=user_in.email,
        password=security.get_password_hash(user_in.password),
        organization=user_in.organization,
        country=user_in.country,
        phoneNumber=user_in.phoneNumber,
        registrationPackage=user_in.registrationPackage
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = security.create_access_token(user.id)
    return schemas.Token(user=user, token=access_token)

@router.post("/login", response_model=schemas.Token)
def login(login_in: schemas.LoginRequest, db: Session = Depends(deps.get_db)):
    user = db.query(models.User).filter(models.User.email == login_in.email).first()
    if not user or not security.verify_password(login_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = security.create_access_token(user.id)
    return schemas.Token(user=user, token=access_token)
