from datetime import date
from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, EmailStr, Field

from app.auth import UserClaims, require_role

router = APIRouter(tags=["doctors"])


class DoctorRegistration(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    medical_license_number: str = Field(min_length=1, max_length=100)
    specialty: str = Field(min_length=1, max_length=200)


class DoctorProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    email: EmailStr | None = None
    specialty: str | None = Field(default=None, min_length=1, max_length=200)


class DoctorAdminUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    specialty: str | None = Field(default=None, min_length=1, max_length=200)
    admin_notes: str | None = Field(default=None, max_length=2000)


class CertificationSubmission(BaseModel):
    certification_name: str = Field(min_length=1, max_length=200)
    issuing_organization: str = Field(min_length=1, max_length=200)
    issue_date: date
    expiration_date: date | None = None
    evidence_reference: str = Field(min_length=1, max_length=2000)


class CertificationRecord(CertificationSubmission):
    id: str
    verification_status: Literal["pending", "approved", "rejected"]


class DoctorProfile(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    medical_license_number: str
    specialty: str
    verification_status: Literal["pending", "approved", "rejected"]


class DoctorVerificationStatus(BaseModel):
    status: Literal["pending", "approved", "rejected"]
    certifications: list[CertificationRecord]


class DoctorList(BaseModel):
    items: list[DoctorProfile]
    total: int


class VerificationDecision(BaseModel):
    decision: Literal["approved", "rejected"]
    notes: str | None = Field(default=None, max_length=2000)


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Doctor persistence and business rules are not implemented",
    )


@router.post(
    "/api/v1/doctors",
    response_model=DoctorProfile,
    status_code=status.HTTP_201_CREATED,
)
async def register_doctor(payload: DoctorRegistration) -> DoctorProfile:
    not_implemented()


@router.get("/api/v1/doctors/me", response_model=DoctorProfile)
async def get_current_doctor(
    user: UserClaims = Depends(require_role("doctor")),
) -> DoctorProfile:
    not_implemented()


@router.patch("/api/v1/doctors/me", response_model=DoctorProfile)
async def update_current_doctor(
    payload: DoctorProfileUpdate,
    user: UserClaims = Depends(require_role("doctor")),
) -> DoctorProfile:
    not_implemented()


@router.post(
    "/api/v1/doctors/me/certifications",
    response_model=CertificationRecord,
    status_code=status.HTTP_201_CREATED,
)
async def submit_certification(
    payload: CertificationSubmission,
    user: UserClaims = Depends(require_role("doctor")),
) -> CertificationRecord:
    not_implemented()


@router.get("/api/v1/doctors/me/verification", response_model=DoctorVerificationStatus)
async def get_own_verification_status(
    user: UserClaims = Depends(require_role("doctor")),
) -> DoctorVerificationStatus:
    not_implemented()


@router.get("/api/v1/admin/doctors", response_model=DoctorList)
async def list_doctors(
    search: str | None = Query(default=None, description="Search doctor name, email, or license"),
    user: UserClaims = Depends(require_role("admin")),
) -> DoctorList:
    not_implemented()


@router.get("/api/v1/admin/doctors/{doctorId}", response_model=DoctorProfile)
async def get_doctor(
    doctor_id: str = Path(alias="doctorId"),
    user: UserClaims = Depends(require_role("admin")),
) -> DoctorProfile:
    not_implemented()


@router.patch(
    "/api/v1/admin/doctors/{doctorId}/verification",
    response_model=DoctorProfile,
)
async def decide_doctor_verification(
    payload: VerificationDecision,
    doctor_id: str = Path(alias="doctorId"),
    user: UserClaims = Depends(require_role("admin")),
) -> DoctorProfile:
    not_implemented()


@router.patch("/api/v1/admin/doctors/{doctorId}", response_model=DoctorProfile)
async def update_doctor_as_admin(
    payload: DoctorAdminUpdate,
    doctor_id: str = Path(alias="doctorId"),
    user: UserClaims = Depends(require_role("admin")),
) -> DoctorProfile:
    not_implemented()
