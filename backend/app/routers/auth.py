from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from databases.session import get_db
from databases.schema.models import User, Doctor, Manufacturer, AuditHistory
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_active_user,
    UserClaims,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["doctor", "manufacturer"]
    # Profile information required for doctor/manufacturer initialization
    full_name_or_company: str = Field(min_length=1, max_length=200)
    medical_license_or_contact_name: str = Field(min_length=1, max_length=200)
    specialty_or_contact_email: str = Field(min_length=1, max_length=255)


class RegisterResponse(BaseModel):
    id: str
    email: str
    role: str
    status: str
    message: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str


class UserMeResponse(BaseModel):
    id: str
    email: str
    role: str
    status: str


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new Doctor or Manufacturer account",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    # 1. Reject public admin registration
    if payload.role not in ("doctor", "manufacturer"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Public registration is restricted to doctor or manufacturer roles.",
        )

    # 2. Check for duplicate email
    existing_user = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists.",
        )

    # 3. Hash password securely
    hashed_pwd = hash_password(payload.password)

    # 4. Create User entity
    new_user = User(
        email=payload.email.lower(),
        hashed_password=hashed_pwd,
        role=payload.role,
        status="active",
    )
    db.add(new_user)
    db.flush()

    # 5. Link core profile depending on role
    if payload.role == "doctor":
        # Check medical license uniqueness
        existing_doc = db.query(Doctor).filter(
            Doctor.medical_license_number == payload.medical_license_or_contact_name
        ).first()
        if existing_doc is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A doctor profile with this medical license number already exists.",
            )

        new_doctor = Doctor(
            user_id=new_user.id,
            full_name=payload.full_name_or_company,
            medical_license_number=payload.medical_license_or_contact_name,
            specialty=payload.specialty_or_contact_email,
            verification_status="pending",
        )
        db.add(new_doctor)
    elif payload.role == "manufacturer":
        new_mfg = Manufacturer(
            user_id=new_user.id,
            company_name=payload.full_name_or_company,
            contact_name=payload.medical_license_or_contact_name,
            contact_email=payload.specialty_or_contact_email,
            verification_status="pending",
        )
        db.add(new_mfg)

    # 6. Audit log entry (without passwords or secrets)
    audit = AuditHistory(
        actor_id=new_user.id,
        action="USER_REGISTRATION",
        target_entity="User",
        target_id=new_user.id,
        details={"role": payload.role, "email": new_user.email},
    )
    db.add(audit)

    db.commit()
    db.refresh(new_user)

    return RegisterResponse(
        id=new_user.id,
        email=new_user.email,
        role=new_user.role,
        status=new_user.status,
        message="Registration successful.",
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and obtain JWT access token",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is suspended or inactive.",
        )

    token = create_access_token(user_id=user.id, role=user.role)

    # Log successful login
    audit = AuditHistory(
        actor_id=user.id,
        action="USER_LOGIN",
        target_entity="User",
        target_id=user.id,
        details={"email": user.email},
    )
    db.add(audit)
    db.commit()

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        role=user.role,
    )


@router.get(
    "/me",
    response_model=UserMeResponse,
    summary="Get current authenticated user profile",
)
def get_me(current_user: User = Depends(get_current_active_user)):
    return UserMeResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        status=current_user.status,
    )
