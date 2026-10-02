from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class RoleEnum(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class PaymentStatusEnum(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class SubmissionStatusEnum(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

# --- User Schemas ---
class UserBase(BaseModel):
    fullName: str
    organization: Optional[str] = None
    country: Optional[str] = None
    phoneNumber: Optional[str] = None
    registrationPackage: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    confirmPassword: str

class UserUpdate(BaseModel):
    fullName: Optional[str] = None
    organization: Optional[str] = None
    country: Optional[str] = None
    phoneNumber: Optional[str] = None

class UserAdminUpdate(BaseModel):
    paymentStatus: PaymentStatusEnum

class UserResponse(UserBase):
    id: UUID
    email: EmailStr
    role: RoleEnum
    paymentStatus: PaymentStatusEnum
    createdAt: datetime
    
    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    user: UserResponse
    token: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- Submission Schemas ---
class SubmissionBase(BaseModel):
    title: str
    subTheme: Optional[str] = None

class SubmissionUserResponse(BaseModel):
    id: UUID
    fullName: str
    email: EmailStr

    class Config:
        from_attributes = True

class SubmissionResponse(SubmissionBase):
    id: UUID
    originalFileName: str
    fileSizeMB: Optional[float] = None
    status: SubmissionStatusEnum
    createdAt: datetime
    user: SubmissionUserResponse
    
    class Config:
        from_attributes = True

# --- Contact Schemas ---
class ContactCreate(BaseModel):
    name: str = Field(..., alias="name")
    email: EmailStr = Field(..., alias="email")
    subject: str
    message: str

class ContactResponse(BaseModel):
    message: str

# --- Pagination Schemas ---
class PaginatedUsersResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    totalPages: int

class AdminStatsResponse(BaseModel):
    totalRegistrations: int
    paymentsCompleted: int
    totalSubmissions: int
    pendingPayments: int
