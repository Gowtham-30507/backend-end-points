from datetime import datetime
from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from app.core.permissions import UserClaims, require_role, require_roles

router = APIRouter(tags=["research submissions"])


class ResearchSubmissionPayload(BaseModel):
    submission_type: Literal["formulation", "medical_details", "case_study"]
    title: str = Field(min_length=1, max_length=300)
    summary: str = Field(min_length=1, max_length=2000)
    content: str = Field(min_length=1, max_length=20000)
    attachments: list[str] = Field(default_factory=list, max_length=20)


class ResearchSubmissionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    summary: str | None = Field(default=None, min_length=1, max_length=2000)
    content: str | None = Field(default=None, min_length=1, max_length=20000)
    attachments: list[str] | None = Field(default=None, max_length=20)


class ResearchSubmission(ResearchSubmissionPayload):
    id: str
    doctor_id: str
    status: Literal["submitted", "under_review", "approved", "rejected", "returned"]
    submitted_at: datetime


class ResearchSubmissionList(BaseModel):
    items: list[ResearchSubmission]
    total: int


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Research submission persistence, authorization, and moderation are not implemented",
    )


@router.post(
    "/api/v1/research-submissions",
    response_model=ResearchSubmission,
    status_code=status.HTTP_201_CREATED,
)
async def submit_research(
    payload: ResearchSubmissionPayload,
    user: UserClaims = Depends(require_role("doctor")),
) -> ResearchSubmission:
    not_implemented()


@router.get(
    "/api/v1/doctors/me/research-submissions",
    response_model=ResearchSubmissionList,
)
async def list_own_research_submissions(
    submission_status: Literal["submitted", "under_review", "approved", "rejected", "returned"]
    | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("doctor")),
) -> ResearchSubmissionList:
    not_implemented()


@router.get(
    "/api/v1/research-submissions/{submissionId}",
    response_model=ResearchSubmission,
)
async def get_research_submission(
    submission_id: str = Path(alias="submissionId"),
    user: UserClaims = Depends(require_roles("doctor", "admin")),
) -> ResearchSubmission:
    not_implemented()


@router.patch(
    "/api/v1/research-submissions/{submissionId}",
    response_model=ResearchSubmission,
)
async def update_research_submission(
    payload: ResearchSubmissionUpdate,
    submission_id: str = Path(alias="submissionId"),
    user: UserClaims = Depends(require_roles("doctor", "admin")),
) -> ResearchSubmission:
    not_implemented()


@router.get(
    "/api/v1/admin/research-submissions",
    response_model=ResearchSubmissionList,
)
async def list_research_submissions_for_admin(
    submission_status: Literal["submitted", "under_review", "approved", "rejected", "returned"]
    | None = Query(default=None, alias="status"),
    submission_type: Literal["formulation", "medical_details", "case_study"] | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> ResearchSubmissionList:
    not_implemented()
