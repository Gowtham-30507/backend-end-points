from datetime import date, datetime
from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from app.core.permissions import UserClaims, require_role

router = APIRouter(tags=["adverse drug reaction reports"])


class AdrReportSubmission(BaseModel):
    product_id: str = Field(min_length=1, max_length=100)
    product_name: str = Field(min_length=1, max_length=300)
    reaction: str = Field(min_length=1, max_length=2000)
    occurred_on: date
    outcome: Literal["recovered", "recovering", "not_recovered", "fatal", "unknown"]
    seriousness: Literal["non_serious", "serious", "life_threatening", "fatal"]
    description: str = Field(min_length=1, max_length=10000)


class AdrReport(AdrReportSubmission):
    id: str
    doctor_id: str
    status: Literal["submitted", "under_review", "closed"]
    submitted_at: datetime


class AdrReportList(BaseModel):
    items: list[AdrReport]
    total: int


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="ADR report persistence, disclosure policy, and summary logic are not implemented",
    )


@router.post(
    "/api/v1/adr-reports",
    response_model=AdrReport,
    status_code=status.HTTP_201_CREATED,
)
async def submit_adr_report(
    payload: AdrReportSubmission,
    user: UserClaims = Depends(require_role("doctor")),
) -> AdrReport:
    not_implemented()


@router.get("/api/v1/admin/adr-reports", response_model=AdrReportList)
async def list_adr_reports(
    report_status: Literal["submitted", "under_review", "closed"] | None = Query(
        default=None, alias="status"
    ),
    product_id: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> AdrReportList:
    not_implemented()


@router.get(
    "/api/v1/manufacturers/me/adr-reports",
    response_model=AdrReportList,
)
async def list_adr_reports_for_manufacturer(
    product_id: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("manufacturer")),
) -> AdrReportList:
    not_implemented()
