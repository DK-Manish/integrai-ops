from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import UUID, uuid4
import bcrypt
from jose import jwt

from app.core.config import get_settings

settings = get_settings()

TokenType = Literal["access", "refresh"]


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt. Passwords longer than 72 bytes are truncated,
    which is bcrypt's own documented limit."""
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against a bcrypt hash."""
    password_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def create_token(user_id: UUID, token_type: TokenType) -> str:
    """Create a signed JWT for a user, either a short-lived access token or longer-lived refresh token."""
    now = datetime.now(timezone.utc)

    if token_type == "access":
        expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "type": token_type,
        "jti": str(uuid4()),
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT. Raises JWTError if invalid, expired, or tampered with."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])