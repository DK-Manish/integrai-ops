from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class AuthError(Exception):
    """Raised for any authentication failure (bad credentials, duplicate email, etc.)."""


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def register_user(db: AsyncSession, data: UserCreate) -> User:
    """Create a new user. Raises AuthError if the email is already registered."""
    existing = await get_user_by_email(db, data.email)
    if existing is not None:
        raise AuthError("A user with this email already exists.")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    """Verify credentials. Raises AuthError if the email doesn't exist, the password is wrong,
    or the account is inactive. The error message is deliberately the same in both the
    'no such user' and 'wrong password' cases, to avoid leaking which emails are registered."""
    user = await get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise AuthError("Incorrect email or password.")
    if not user.is_active:
        raise AuthError("This account has been deactivated.")
    return user