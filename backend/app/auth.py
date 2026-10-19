import os
from collections.abc import Callable
from typing import Literal, NoReturn, TypedDict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer(auto_error=False)


class UserClaims(TypedDict):
    sub: str
    role: Literal["manufacturer", "doctor", "admin"]


Role = Literal["manufacturer", "doctor", "admin"]


def require_roles(*required_roles: Role) -> Callable[..., UserClaims]:
    if not required_roles:
        raise ValueError("At least one role must be provided")

    def authenticate(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    ) -> UserClaims:
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer token required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        secret = os.getenv("JWT_SECRET_KEY")
        if secret is None or len(secret.encode("utf-8")) < 32:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="JWT authentication is not configured",
            )

        try:
            claims = jwt.decode(credentials.credentials, secret, algorithms=["HS256"])
        except jwt.InvalidTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid bearer token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        subject = claims.get("sub")
        role = claims.get("role")
        if not isinstance(subject, str) or role not in ("manufacturer", "doctor", "admin"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid bearer token claims",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return {"sub": subject, "role": role}

    return authenticate


def require_role(required_role: Role) -> Callable[..., UserClaims]:
    return require_roles(required_role)
