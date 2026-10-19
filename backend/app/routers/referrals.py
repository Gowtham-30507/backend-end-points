from datetime import datetime
from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.auth import UserClaims, require_role

router = APIRouter(tags=["referrals"])


class ReferralSubmission(BaseModel):
    referred_name: str = Field(min_length=1, max_length=200)
    referred_contact: str = Field(min_length=1, max_length=320)
    reason: str = Field(min_length=1, max_length=2000)


class ReferralRecord(ReferralSubmission):
    id: str
    referring_doctor_id: str
    status: Literal["submitted", "accepted", "completed", "declined"]
    score_awarded: int = Field(default=0, ge=0)
    created_at: datetime
    updated_at: datetime


class ReferralList(BaseModel):
    items: list[ReferralRecord]
    total: int


class ReferralScore(BaseModel):
    doctor_id: str
    score: int = Field(ge=0)
    referral_count: int = Field(ge=0)


class ReferralLeaderboardEntry(ReferralScore):
    doctor_name: str
    rank: int = Field(ge=1)


class ReferralLeaderboard(BaseModel):
    items: list[ReferralLeaderboardEntry]
    total: int


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Referral persistence, scoring rules, and business workflows are not implemented",
    )


@router.post(
    "/api/v1/referrals",
    response_model=ReferralRecord,
    status_code=status.HTTP_201_CREATED,
)
async def create_referral(
    payload: ReferralSubmission,
    user: UserClaims = Depends(require_role("doctor")),
) -> ReferralRecord:
    not_implemented()


@router.get("/api/v1/doctors/me/referrals", response_model=ReferralList)
async def list_own_referrals(
    referral_status: Literal["submitted", "accepted", "completed", "declined"] | None = Query(
        default=None, alias="status"
    ),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("doctor")),
) -> ReferralList:
    not_implemented()


@router.get("/api/v1/doctors/me/referral-score", response_model=ReferralScore)
async def get_own_referral_score(
    user: UserClaims = Depends(require_role("doctor")),
) -> ReferralScore:
    not_implemented()


@router.get("/api/v1/admin/referrals", response_model=ReferralList)
async def list_referrals_for_admin(
    referral_status: Literal["submitted", "accepted", "completed", "declined"] | None = Query(
        default=None, alias="status"
    ),
    doctor_id: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> ReferralList:
    not_implemented()


@router.get("/api/v1/admin/referral-leaderboard", response_model=ReferralLeaderboard)
async def get_referral_leaderboard(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> ReferralLeaderboard:
    not_implemented()
