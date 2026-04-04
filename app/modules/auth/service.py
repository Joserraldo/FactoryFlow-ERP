import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.modules.auth.models import User, UserRole
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import TokenResponse, UserCreate

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.repo = AuthRepository(db)

    def register(self, data: UserCreate) -> User:
        """Register a new user. Raises 400 if username or email already exists."""
        if self.repo.get_by_username(data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Validate role
        try:
            role = UserRole(data.role)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role: {data.role}")

        user = User(
            username=data.username,
            email=data.email,
            password_hash=get_password_hash(data.password),
            role=role,
        )
        user = self.repo.create_user(user)
        logger.info("User registered: %s (role=%s)", user.username, user.role.value)
        return user

    def login(self, username: str, password: str) -> TokenResponse:
        """Authenticate and return access + refresh tokens. Stores refresh token in DB."""
        user = self.repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        # Persist refresh token
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.repo.store_refresh_token(user_id=user.id, token=refresh_token, expires_at=expires_at)

        logger.info("User logged in: %s", user.username)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh(self, refresh_token: str) -> TokenResponse:
        """Validate refresh token from DB, rotate it, return new token pair."""
        # Decode
        payload = decode_token(refresh_token, is_refresh=True)
        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # Verify in DB
        stored = self.repo.get_refresh_token(refresh_token)
        if stored is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked or not found")

        if stored.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        user_id = payload["sub"]

        # Revoke old token
        self.repo.revoke_refresh_token(refresh_token)

        # Issue new pair
        new_access = create_access_token(subject=user_id)
        new_refresh = create_refresh_token(subject=user_id)

        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.repo.store_refresh_token(user_id=user_id, token=new_refresh, expires_at=expires_at)

        logger.info("Token refreshed for user: %s", user_id)
        return TokenResponse(access_token=new_access, refresh_token=new_refresh)
