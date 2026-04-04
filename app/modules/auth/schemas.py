import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, constr


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # type: ignore[valid-type]
    email: EmailStr
    password: constr(min_length=6)  # type: ignore[valid-type]
    role: str = "admin"


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
