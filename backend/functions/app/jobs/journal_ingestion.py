from datetime import datetime
from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from app.core.permissions import UserClaims, require_role

router = APIRouter(tags=["journal ingestion"])


class JournalIngestionRunRequest(BaseModel):
    source: str = Field(min_length=1, max_length=200)
    query: str | None = Field(default=None, max_length=1000)


class JournalIngestionRun(BaseModel):
    id: str
    source: str
    status: Literal["queued", "running", "completed", "failed"]
    started_at: datetime | None = None
    completed_at: datetime | None = None
    records_fetched: int = Field(default=0, ge=0)
    records_created: int = Field(default=0, ge=0)
    records_updated: int = Field(default=0, ge=0)
    error: str | None = None


class JournalIngestionRunList(BaseModel):
    items: list[JournalIngestionRun]
    total: int


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Journal ingestion workflow and external API integration are not implemented",
    )


@router.post(
    "/api/v1/admin/journal-ingestion-runs",
    response_model=JournalIngestionRun,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_journal_ingestion(
    payload: JournalIngestionRunRequest,
    user: UserClaims = Depends(require_role("admin")),
) -> JournalIngestionRun:
    not_implemented()


@router.get(
    "/api/v1/admin/journal-ingestion-runs",
    response_model=JournalIngestionRunList,
)
async def list_journal_ingestion_runs(
    run_status: Literal["queued", "running", "completed", "failed"] | None = Query(
        default=None, alias="status"
    ),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> JournalIngestionRunList:
    not_implemented()


@router.get(
    "/api/v1/admin/journal-ingestion-runs/{runId}",
    response_model=JournalIngestionRun,
)
async def get_journal_ingestion_run(
    run_id: str = Path(alias="runId"),
    user: UserClaims = Depends(require_role("admin")),
) -> JournalIngestionRun:
    not_implemented()
