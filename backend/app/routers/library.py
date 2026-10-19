from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from app.auth import UserClaims, require_role

router = APIRouter(tags=["library"])


class LibraryEntrySubmission(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    summary: str = Field(min_length=1, max_length=2000)
    content: str = Field(min_length=1, max_length=20000)
    category: str = Field(min_length=1, max_length=100)
    source_references: list[str] = Field(default_factory=list, max_length=20)


class LibraryEntryUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    summary: str | None = Field(default=None, min_length=1, max_length=2000)
    content: str | None = Field(default=None, min_length=1, max_length=20000)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    source_references: list[str] | None = Field(default=None, max_length=20)
    is_published: bool | None = None


class LibraryEntry(LibraryEntrySubmission):
    id: str
    is_published: bool = True


class LibraryEntryList(BaseModel):
    items: list[LibraryEntry]
    total: int


class LibraryContributionSubmission(LibraryEntrySubmission):
    pass


class LibraryContribution(LibraryContributionSubmission):
    id: str
    doctor_id: str
    decision: Literal["pending", "approved", "rejected", "returned"]
    reviewer_notes: str | None = None


class LibraryContributionList(BaseModel):
    items: list[LibraryContribution]
    total: int


class ContributionDecision(BaseModel):
    decision: Literal["approved", "rejected", "returned"]
    notes: str | None = Field(default=None, max_length=2000)


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Library persistence and contribution workflow are not implemented",
    )


@router.get("/api/v1/library/entries", response_model=LibraryEntryList)
async def browse_library_entries(
    search: str | None = Query(default=None, description="Search library entry title or content"),
    category: str | None = Query(default=None, min_length=1, max_length=100),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> LibraryEntryList:
    not_implemented()


@router.get("/api/v1/library/entries/{entryId}", response_model=LibraryEntry)
async def get_library_entry(
    entry_id: str = Path(alias="entryId"),
) -> LibraryEntry:
    not_implemented()


@router.post(
    "/api/v1/library/contributions",
    response_model=LibraryContribution,
    status_code=status.HTTP_201_CREATED,
)
async def submit_library_contribution(
    payload: LibraryContributionSubmission,
    user: UserClaims = Depends(require_role("doctor")),
) -> LibraryContribution:
    not_implemented()


@router.get(
    "/api/v1/doctors/me/library-contributions",
    response_model=LibraryContributionList,
)
async def list_own_library_contributions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("doctor")),
) -> LibraryContributionList:
    not_implemented()


@router.get("/api/v1/admin/library/entries", response_model=LibraryEntryList)
async def list_library_entries_for_admin(
    search: str | None = Query(default=None, description="Search library entry title or content"),
    is_published: bool | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> LibraryEntryList:
    not_implemented()


@router.post(
    "/api/v1/admin/library/entries",
    response_model=LibraryEntry,
    status_code=status.HTTP_201_CREATED,
)
async def create_library_entry(
    payload: LibraryEntrySubmission,
    user: UserClaims = Depends(require_role("admin")),
) -> LibraryEntry:
    not_implemented()


@router.patch(
    "/api/v1/admin/library/entries/{entryId}",
    response_model=LibraryEntry,
)
async def update_library_entry(
    payload: LibraryEntryUpdate,
    entry_id: str = Path(alias="entryId"),
    user: UserClaims = Depends(require_role("admin")),
) -> LibraryEntry:
    not_implemented()


@router.get(
    "/api/v1/admin/library/contributions",
    response_model=LibraryContributionList,
)
async def list_library_contributions_for_admin(
    decision: Literal["pending", "approved", "rejected", "returned"] | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> LibraryContributionList:
    not_implemented()


@router.patch(
    "/api/v1/admin/library/contributions/{contributionId}/decision",
    response_model=LibraryContribution,
)
async def decide_library_contribution(
    payload: ContributionDecision,
    contribution_id: str = Path(alias="contributionId"),
    user: UserClaims = Depends(require_role("admin")),
) -> LibraryContribution:
    not_implemented()
