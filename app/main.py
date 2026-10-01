from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="AEAA Conference Portal API",
    description="Backend API for the 43rd AEAA Conference Portal",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def startup_event():
    from app.database import engine, Base, SessionLocal
    from app.models import User, RoleEnum
    from app.core.security import get_password_hash
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Ensure admin user exists
    db = SessionLocal()
    try:
        admin_email = "aeaa2027@neco.gov.ng"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            new_admin = User(
                fullName="System Administrator",
                email=admin_email,
                password=get_password_hash("Admin@123"),
                role=RoleEnum.ADMIN
            )
            db.add(new_admin)
            db.commit()
            print(f"Auto-created admin user: {admin_email}")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AEAA Conference Portal API"}

from app.routers import auth, user, admin, contact
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(contact.router, prefix="/api/contact", tags=["contact"])

# Routers will be included here
