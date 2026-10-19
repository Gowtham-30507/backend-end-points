from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, EmailStr, Field

from app.auth import UserClaims, require_role

router = APIRouter(tags=["manufacturers"])


class ManufacturerRegistration(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    contact_name: str = Field(min_length=1, max_length=200)
    contact_email: EmailStr


class ManufacturerProfileUpdate(BaseModel):
    contact_name: str | None = Field(default=None, min_length=1, max_length=200)
    contact_email: EmailStr | None = None


class ManufacturerProfile(BaseModel):
    id: str
    company_name: str
    contact_name: str
    contact_email: str
    verification_status: Literal["pending", "approved", "rejected"]


class ManufacturerList(BaseModel):
    items: list[ManufacturerProfile]
    total: int


class VerificationDecision(BaseModel):
    decision: Literal["approved", "rejected"]
    notes: str | None = Field(default=None, max_length=2000)


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Manufacturer persistence and business rules are not implemented",
    )


@router.post(
    "/api/v1/manufacturers",
    response_model=ManufacturerProfile,
    status_code=status.HTTP_201_CREATED,
)
async def register_manufacturer(payload: ManufacturerRegistration) -> ManufacturerProfile:
    not_implemented()


@router.get("/api/v1/manufacturers/me", response_model=ManufacturerProfile)
async def get_current_manufacturer(
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ManufacturerProfile:
    not_implemented()


@router.patch("/api/v1/manufacturers/me", response_model=ManufacturerProfile)
async def update_current_manufacturer(
    payload: ManufacturerProfileUpdate,
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ManufacturerProfile:
    not_implemented()


@router.get("/api/v1/admin/manufacturers", response_model=ManufacturerList)
async def list_manufacturers(
    search: str | None = Query(default=None, description="Search manufacturer name or email"),
    user: UserClaims = Depends(require_role("admin")),
) -> ManufacturerList:
    not_implemented()


@router.get(
    "/api/v1/admin/manufacturers/{manufacturerId}",
    response_model=ManufacturerProfile,
)
async def get_manufacturer(
    manufacturer_id: str = Path(alias="manufacturerId"),
    user: UserClaims = Depends(require_role("admin")),
) -> ManufacturerProfile:
    not_implemented()


@router.patch(
    "/api/v1/admin/manufacturers/{manufacturerId}/verification",
    response_model=ManufacturerProfile,
)
async def decide_manufacturer_verification(
    payload: VerificationDecision,
    manufacturer_id: str = Path(alias="manufacturerId"),
    user: UserClaims = Depends(require_role("admin")),
) -> ManufacturerProfile:
    not_implemented()
