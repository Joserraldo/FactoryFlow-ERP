import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, constr


# ---- Unit Schemas ----

class UnitOut(BaseModel):
    id: uuid.UUID
    name: str
    symbol: str

    model_config = ConfigDict(from_attributes=True)


# ---- Material Schemas ----

class MaterialCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    primary_unit_id: uuid.UUID
    secondary_unit_id: uuid.UUID
    conversion_factor: float
    stock_primary: float = 0.0
    cost_cpp: float = 0.0


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    primary_unit_id: Optional[uuid.UUID] = None
    secondary_unit_id: Optional[uuid.UUID] = None
    conversion_factor: Optional[float] = None


class MaterialOut(BaseModel):
    id: uuid.UUID
    name: str
    primary_unit_id: uuid.UUID
    secondary_unit_id: uuid.UUID
    conversion_factor: float
    stock_primary: float
    stock_secondary: float
    cost_cpp: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
