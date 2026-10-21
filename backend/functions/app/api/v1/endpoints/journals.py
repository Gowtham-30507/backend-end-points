from datetime import date, datetime
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from pydantic import BaseModel, Field, HttpUrl

from app.core.permissions import UserClaims, require_role

router = APIRouter(tags=["journals"])


class JournalRecordSubmission(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    authors: list[str] = Field(default_factory=list, max_length=100)
    journal_name: str = Field(min_length=1, max_length=300)
    publication_date: date | None = None
    doi: str | None = Field(default=None, max_length=200)
    url: HttpUrl | None = None
    abstract: str | None = Field(default=None, max_length=20000)


class JournalRecordUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    authors: list[str] | None = Field(default=None, max_length=100)
    journal_name: str | None = Field(default=None, min_length=1, max_length=300)
    publication_date: date | None = None
    doi: str | None = Field(default=None, max_length=200)
    url: HttpUrl | None = None
    abstract: str | None = Field(default=None, max_length=20000)


class JournalRecord(JournalRecordSubmission):
    id: str
    created_at: datetime
    updated_at: datetime


class JournalRecordList(BaseModel):
    items: list[JournalRecord]
    total: int


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Journal persistence is not implemented",
    )


@router.get("/api/v1/journals", response_model=JournalRecordList)
async def browse_journals(
    search: str | None = Query(default=None, description="Search journal title, authors, or DOI"),
    journal_name: str | None = Query(default=None, min_length=1, max_length=300),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> JournalRecordList:
    not_implemented()


@router.get("/api/v1/journals/{journalId}", response_model=JournalRecord)
async def get_journal(
    journal_id: str = Path(alias="journalId"),
) -> JournalRecord:
    not_implemented()


@router.get("/api/v1/admin/journals", response_model=JournalRecordList)
async def list_journals_for_admin(
    search: str | None = Query(default=None, description="Search journal title, authors, or DOI"),
    journal_name: str | None = Query(default=None, min_length=1, max_length=300),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> JournalRecordList:
    not_implemented()


@router.post(
    "/api/v1/admin/journals",
    response_model=JournalRecord,
    status_code=status.HTTP_201_CREATED,
)
async def create_journal(
    payload: JournalRecordSubmission,
    user: UserClaims = Depends(require_role("admin")),
) -> JournalRecord:
    not_implemented()


@router.patch(
    "/api/v1/admin/journals/{journalId}",
    response_model=JournalRecord,
)
async def update_journal(
    payload: JournalRecordUpdate,
    journal_id: str = Path(alias="journalId"),
    user: UserClaims = Depends(require_role("admin")),
) -> JournalRecord:
    not_implemented()


@router.delete(
    "/api/v1/admin/journals/{journalId}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_journal(
    journal_id: str = Path(alias="journalId"),
    user: UserClaims = Depends(require_role("admin")),
) -> Response:
    not_implemented()

