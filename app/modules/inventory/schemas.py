import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MovementCreate(BaseModel):
    material_id: uuid.UUID
    type: str  # "IN" or "OUT"
    quantity_primary: float
    unit_cost: float = 0.0


class MovementOut(BaseModel):
    id: uuid.UUID
    material_id: uuid.UUID
    type: str
    quantity_primary: float
    quantity_secondary: float
    unit_cost: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
