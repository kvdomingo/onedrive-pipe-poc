import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.settings import settings

bearer_scheme = HTTPBearer(auto_error=False)


def require_bearer(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> None:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization"
        )

    expected = settings.WEBHOOK_SECRET.get_secret_value()

    if not secrets.compare_digest(credentials.credentials, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
