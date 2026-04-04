import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ---- Consumption ----

class ConsumptionOut(BaseModel):
    id: uuid.UUID
    material_id: uuid.UUID
    quantity_used: float

    model_config = ConfigDict(from_attributes=True)


# ---- Production Order ----

class ProductionOrderCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int


class ProductionOrderOut(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    status: str
    created_at: datetime
    consumptions: List[ConsumptionOut] = []

    model_config = ConfigDict(from_attributes=True)
