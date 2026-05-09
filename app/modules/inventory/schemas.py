import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MovementCreate(BaseModel):
    material_id: uuid.UUID
    type: str  # "IN" or "OUT"
    quantity_primary: float
    unit_cost: float = 0.0
    supplier_id: Optional[uuid.UUID] = None


class MovementOut(BaseModel):
    id: uuid.UUID
    material_id: uuid.UUID
    type: str
    quantity_primary: float
    quantity_secondary: float
    unit_cost: float
    supplier_id: Optional[uuid.UUID]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
