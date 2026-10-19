from typing import Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from app.auth import UserClaims, require_role

router = APIRouter(tags=["products"])


class ProductSubmission(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=5000)
    category: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class ProductAdminUpdate(ProductUpdate):
    is_active: bool | None = None
    admin_notes: str | None = Field(default=None, max_length=2000)


class ProductRecord(ProductSubmission):
    id: str
    manufacturer_id: str
    approval_status: Literal["pending", "approved", "rejected"]
    is_active: bool = True


class ProductList(BaseModel):
    items: list[ProductRecord]
    total: int


class ProductApprovalDecision(BaseModel):
    decision: Literal["approved", "rejected"]
    notes: str | None = Field(default=None, max_length=2000)


def not_implemented() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Product persistence and business rules are not implemented",
    )


@router.get("/api/v1/products", response_model=ProductList)
async def browse_products(
    search: str | None = Query(default=None, description="Search approved product name or description"),
    category: str | None = Query(default=None, min_length=1, max_length=100),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ProductList:
    not_implemented()


@router.get("/api/v1/products/{productId}", response_model=ProductRecord)
async def get_product(
    product_id: str = Path(alias="productId"),
) -> ProductRecord:
    not_implemented()


@router.post(
    "/api/v1/manufacturers/me/products",
    response_model=ProductRecord,
    status_code=status.HTTP_201_CREATED,
)
async def submit_product(
    payload: ProductSubmission,
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ProductRecord:
    not_implemented()


@router.get("/api/v1/manufacturers/me/products", response_model=ProductList)
async def list_own_products(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ProductList:
    not_implemented()


@router.patch(
    "/api/v1/manufacturers/me/products/{productId}",
    response_model=ProductRecord,
)
async def update_own_product(
    payload: ProductUpdate,
    product_id: str = Path(alias="productId"),
    user: UserClaims = Depends(require_role("manufacturer")),
) -> ProductRecord:
    not_implemented()


@router.get("/api/v1/admin/products", response_model=ProductList)
async def list_products_for_admin(
    search: str | None = Query(default=None, description="Search product name or description"),
    approval_status: Literal["pending", "approved", "rejected"] | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: UserClaims = Depends(require_role("admin")),
) -> ProductList:
    not_implemented()


@router.patch(
    "/api/v1/admin/products/{productId}/approval",
    response_model=ProductRecord,
)
async def decide_product_approval(
    payload: ProductApprovalDecision,
    product_id: str = Path(alias="productId"),
    user: UserClaims = Depends(require_role("admin")),
) -> ProductRecord:
    not_implemented()


@router.patch("/api/v1/admin/products/{productId}", response_model=ProductRecord)
async def update_product_as_admin(
    payload: ProductAdminUpdate,
    product_id: str = Path(alias="productId"),
    user: UserClaims = Depends(require_role("admin")),
) -> ProductRecord:
    not_implemented()
