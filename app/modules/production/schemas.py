"""
===============================================================================
Archivo: schemas.py
Propósito: Data Transfer Objects (DTOs) para Producción.
Rol Arquitectónico: Validar los payloads de entrada para la creación de órdenes,
                   incluyendo asignaciones de usuarios a pasos específicos.
===============================================================================
"""

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# =============================================================================
# Esquemas de Consumo
# =============================================================================

class ConsumptionOut(BaseModel):
    """Esquema de salida para el registro inmutable de consumo de materiales."""
    id: uuid.UUID
    material_id: uuid.UUID
    quantity_used: float
    quantity_used_secondary: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Esquemas de Órdenes de Producción
# =============================================================================

class StepAssignmentCreate(BaseModel):
    """DTO para asignar dinámicamente un operario a un proceso de la receta."""
    process_id: uuid.UUID
    assigned_to: Optional[uuid.UUID] = None


class ProductionOrderCreate(BaseModel):
    """
    DTO para iniciar un lote de producción.
    Solo requiere el ID del producto final, la cantidad y opcionalmente 
    quiénes harán cada paso. El sistema inferirá el consumo automáticamente.
    """
    product_id: uuid.UUID
    quantity: int
    step_assignments: List[StepAssignmentCreate] = []


class ProductionStepOut(BaseModel):
    """Respuesta de estado de un paso de producción particular."""
    id: uuid.UUID
    process_id: uuid.UUID
    assigned_to: Optional[uuid.UUID] = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ProductionOrderOut(BaseModel):
    """Esquema maestro de respuesta para la orden de producción."""
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    status: str
    created_at: datetime
    consumptions: List[ConsumptionOut] = []
    steps: List[ProductionStepOut] = []

    model_config = ConfigDict(from_attributes=True)
