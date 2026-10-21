from datetime import datetime
from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from app.core.permissions import UserClaims, require_role

router = APIRouter(tags=["feedback"])


class FeedbackSubmission(BaseModel):
    category: Literal["product", "service", "website", "other"]
    subject: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=10000)


class FeedbackUpdate(BaseModel):
    status: Literal["new", "in_review", "resolved", "dismissed"] | None = None
    admin_notes: str | None = Field(default=None, max_length=2000)


class FeedbackRecord(FeedbackSubmission):
    id: str
    doctor_id: str
    status: Literal["new", "in_review", "resolved", "dismissed"]
    admin_notes: str | None = None
    submitted_at: datetime


class FeedbackList(BaseModel):
    items: list[FeedbackRecord]
    total: int


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Feedback persistence and management are not implemented",
    )


@router.post(
    "/api/v1/feedback",
    response_model=FeedbackRecord,
    status_code=status.HTTP_201_CREATED,
)
async def submit_feedback(
    payload: FeedbackSubmission,
    user: UserClaims = Depends(require_role("doctor")),
) -> FeedbackRecord:
    not_implemented()


@router.get("/api/v1/admin/feedback", response_model=FeedbackList)
async def list_feedback(
    feedback_status: Literal["new", "in_review", "resolved", "dismissed"] | None = Query(
        default=None, alias="status"
    ),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> FeedbackList:
    not_implemented()


@router.patch(
    "/api/v1/admin/feedback/{feedbackId}",
    response_model=FeedbackRecord,
)
async def update_feedback(
    payload: FeedbackUpdate,
    feedback_id: str = Path(alias="feedbackId"),
    user: UserClaims = Depends(require_role("admin")),
) -> FeedbackRecord:
    not_implemented()
