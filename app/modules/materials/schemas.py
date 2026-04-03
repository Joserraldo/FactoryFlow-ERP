from pydantic import BaseModel, ConfigDict
import uuid

class MaterialCreate(BaseModel):
    name: str
    primary_unit_id: uuid.UUID
    secondary_unit_id: uuid.UUID
    conversion_factor: float
    stock_primary: float = 0.0
    cost_cpp: float = 0.0

class MaterialOut(BaseModel):
    id: uuid.UUID
    name: str
    stock_primary: float
    stock_secondary: float
    cost_cpp: float

    model_config = ConfigDict(from_attributes=True)
