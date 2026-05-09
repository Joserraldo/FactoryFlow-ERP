import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, constr


# ---- BOM Item Schemas ----

class BOMItemCreate(BaseModel):
    material_id: uuid.UUID
    quantity_required: float


class BOMItemOut(BaseModel):
    id: uuid.UUID
    material_id: uuid.UUID
    quantity_required: float

    model_config = ConfigDict(from_attributes=True)


# ---- Product Process Schemas ----

class ProductProcessCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    order_index: int = 0


class ProductProcessOut(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    name: str
    order_index: int

    model_config = ConfigDict(from_attributes=True)


# ---- Product Schemas ----

class ProductCreate(BaseModel):
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    sale_price: float
    bom_items: List[BOMItemCreate] = []
    processes: List[ProductProcessCreate] = []


class ProductOut(BaseModel):
    id: uuid.UUID
    name: str
    sale_price: float
    current_stock: float
    created_at: datetime
    bom_items: List[BOMItemOut] = []
    processes: List[ProductProcessOut] = []

    model_config = ConfigDict(from_attributes=True)
