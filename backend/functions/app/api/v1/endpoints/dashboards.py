from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.core.permissions import UserClaims, require_role

router = APIRouter(tags=["dashboards"])


class AdminDashboardSummary(BaseModel):
    registered_doctors: int = Field(ge=0)
    verified_doctors: int = Field(ge=0)
    registered_manufacturers: int = Field(ge=0)
    verified_manufacturers: int = Field(ge=0)
    approved_products: int = Field(ge=0)


class TerritoryCounts(BaseModel):
    territory: str
    doctor_count: int = Field(ge=0)
    manufacturer_count: int = Field(ge=0)


class TerritorySummary(BaseModel):
    items: list[TerritoryCounts]
    total: int = Field(ge=0)


class ManufacturerDashboardSummary(BaseModel):
    approved_products: int = Field(ge=0)
    pending_products: int = Field(ge=0)
    rejected_products: int = Field(ge=0)
    doctor_feedback_count: int = Field(ge=0)


class FeedbackCategorySummary(BaseModel):
    category: str
    count: int = Field(ge=0)


class ManufacturerFeedbackSummary(BaseModel):
    total_feedback: int = Field(ge=0)
    categories: list[FeedbackCategorySummary]


class ManufacturerTerritoryCounts(BaseModel):
    territory: str
    doctor_count: int = Field(ge=0)


class ManufacturerTerritorySummary(BaseModel):
    items: list[ManufacturerTerritoryCounts]
    total: int = Field(ge=0)


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Dashboard metrics and permitted data visibility are not implemented",
    )


@router.get("/api/v1/admin/dashboard/summary", response_model=AdminDashboardSummary)
async def get_admin_dashboard_summary(
    user: UserClaims = Depends(require_role("admin")),
) -> AdminDashboardSummary:
    not_implemented()


@router.get("/api/v1/admin/territories/summary", response_model=TerritorySummary)
async def get_admin_territory_summary(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> TerritorySummary:
    not_implemented()


@router.get(
    "/api/v1/manufacturers/me/dashboard",
    response_model=ManufacturerDashboardSummary,
)
async def get_manufacturer_dashboard(
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ManufacturerDashboardSummary:
    not_implemented()


@router.get(
    "/api/v1/manufacturers/me/doctor-feedback-summary",
    response_model=ManufacturerFeedbackSummary,
)
async def get_manufacturer_doctor_feedback_summary(
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ManufacturerFeedbackSummary:
    not_implemented()


@router.get(
    "/api/v1/manufacturers/me/territory-summary",
    response_model=ManufacturerTerritorySummary,
)
async def get_manufacturer_territory_summary(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ManufacturerTerritorySummary:
    not_implemented()
