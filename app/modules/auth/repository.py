import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.modules.auth.models import RefreshToken, User


class AuthRepository:
    """Data-access layer for Users and RefreshTokens."""

    def __init__(self, db: Session):
        self.db = db

    # ---- Users ----

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ---- Refresh Tokens ----

    def store_refresh_token(self, user_id: uuid.UUID, token: str, expires_at: datetime) -> RefreshToken:
        rt = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        self.db.add(rt)
        self.db.commit()
        return rt

    def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        return self.db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.revoked == False,  # noqa: E712
        ).first()

    def revoke_refresh_token(self, token: str) -> None:
        rt = self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if rt:
            rt.revoked = True
            self.db.commit()

    def revoke_all_user_tokens(self, user_id: uuid.UUID) -> None:
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,  # noqa: E712
        ).update({"revoked": True})
        self.db.commit()
