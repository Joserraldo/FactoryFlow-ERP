import uuid
from datetime import datetime
from typing import Optional

from typing import Optional, List

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


# ---- Sale Items ----

class SaleItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: float
    unit_price: float


class SaleItemOut(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: float
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


# ---- Sale Schemas ----

class SaleCreate(BaseModel):
    client_id: uuid.UUID
    items: List[SaleItemCreate]


class SaleOut(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    total: float
    created_at: datetime
    items: List[SaleItemOut]

    model_config = ConfigDict(from_attributes=True)
