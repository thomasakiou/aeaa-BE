import uuid
from sqlalchemy import Column, String, text, Enum, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class PaymentStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class SubmissionStatusEnum(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullName = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    phoneNumber = Column(String(30), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    registrationPackage = Column(String(100), nullable=True)
    paymentStatus = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    submissions = relationship("PaperSubmission", back_populates="user", cascade="all, delete-orphan")

class PaperSubmission(Base):
    __tablename__ = "paper_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    subTheme = Column(String(255), nullable=True)
    filePath = Column(String(500), nullable=False)
    originalFileName = Column(String(255), nullable=False)
    fileSizeMB = Column(Numeric(6, 2), nullable=True)
    status = Column(Enum(SubmissionStatusEnum), default=SubmissionStatusEnum.SUBMITTED, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="submissions")

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    senderName = Column(String(255), nullable=False)
    senderEmail = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(String, nullable=False)  # TEXT
    sentAt = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
