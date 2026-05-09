import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ---- Consumption ----

class ConsumptionOut(BaseModel):
    id: uuid.UUID
    material_id: uuid.UUID
    quantity_used: float
    quantity_used_secondary: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


# ---- Production Order Schemas ----

class StepAssignmentCreate(BaseModel):
    process_id: uuid.UUID
    assigned_to: Optional[uuid.UUID] = None


class ProductionOrderCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int
    step_assignments: List[StepAssignmentCreate] = []


class ProductionStepOut(BaseModel):
    id: uuid.UUID
    process_id: uuid.UUID
    assigned_to: Optional[uuid.UUID] = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ProductionOrderOut(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    status: str
    created_at: datetime
    consumptions: List[ConsumptionOut] = []
    steps: List[ProductionStepOut] = []

    model_config = ConfigDict(from_attributes=True)
