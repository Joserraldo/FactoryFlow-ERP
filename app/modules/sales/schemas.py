import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, constr


# ---- Client Schemas ----

class ClientCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    email: Optional[EmailStr] = None


class ClientOut(BaseModel):
    id: uuid.UUID
    name: str
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ---- Sale Schemas ----

class SaleCreate(BaseModel):
    client_id: uuid.UUID
    total: float


class SaleOut(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    total: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
