from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_refresh_token
from app.core.config import get_settings
from app.core.security import create_token, decode_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserRead
from app.services.auth_service import AuthError, authenticate_user, get_user_by_id, register_user

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Set the refresh token as an HttpOnly cookie, per OD-01."""
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    try:
        return await register_user(db, data)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, response: Response, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        user = await authenticate_user(db, data.email, data.password)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    access_token = create_token(user.id, "access")
    refresh_token = create_token(user.id, "refresh")
    _set_refresh_cookie(response, refresh_token)

    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    response: Response,
    refresh_token: str = Depends(get_refresh_token),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    invalid_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token."
    )

    try:
        payload = decode_token(refresh_token)
    except Exception:
        raise invalid_error

    if payload.get("type") != "refresh":
        raise invalid_error

    user_id = payload.get("sub")
    if user_id is None:
        raise invalid_error

    from uuid import UUID
    user = await get_user_by_id(db, UUID(user_id))

    user = await get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise invalid_error

    new_access_token = create_token(user.id, "access")
    new_refresh_token = create_token(user.id, "refresh")
    _set_refresh_cookie(response, new_refresh_token)

    return TokenResponse(access_token=new_access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.delete_cookie(key="refresh_token", path="/api/v1/auth")


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user