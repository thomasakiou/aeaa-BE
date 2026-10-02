from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Base
    PROJECT_NAME: str = "AEAA Conference Portal"
    
    # DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:ebimobowei81@localhost:5432/aeaa_db")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-256-bit-secret") # Should be overridden in prod
    JWT_EXPIRY: int = int(os.getenv("JWT_EXPIRY", "60")) # minutes
    
    # SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST", "mail.neco.gov.ng")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USER: str = os.getenv("SMTP_USER", "noreply@neco.gov.ng")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@neco.gov.ng")
    CONTACT_EMAIL: str = os.getenv("CONTACT_EMAIL", "aeaa2027@neco.gov.ng")
    
    # Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "20"))
    
    # Server
    PORT: int = int(os.getenv("PORT", "4000"))
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "https://aeaaafrica.netlify.app")

    class Config:
        env_file = ".env"

settings = Settings()
