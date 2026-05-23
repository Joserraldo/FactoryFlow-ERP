"""
===============================================================================
Archivo: schemas.py
Propósito: Definición de esquemas de datos (DTOs) usando Pydantic.
Rol Arquitectónico: Data Transfer Objects. Validan la entrada del usuario y 
                   formatean las respuestas JSON de salida.
===============================================================================
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, constr


# =============================================================================
# Esquemas de Unidades de Medida
# =============================================================================

class UnitOut(BaseModel):
    """Esquema de salida para Unidades de Medida."""
    id: uuid.UUID
    name: str
    symbol: str

    # Permite a Pydantic leer datos directamente de un modelo SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Esquemas de Proveedores
# =============================================================================

class SupplierCreate(BaseModel):
    """Esquema para la creación de un nuevo proveedor."""
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    contact_email: Optional[str] = None
    phone: Optional[str] = None


class SupplierOut(BaseModel):
    """Esquema de salida para Proveedores."""
    id: uuid.UUID
    name: str
    contact_email: Optional[str]
    phone: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

# =============================================================================
# Esquemas de Materia Prima
# =============================================================================

class MaterialCreate(BaseModel):
    """Esquema para el registro de una nueva Materia Prima."""
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    primary_unit_id: uuid.UUID
    secondary_unit_id: uuid.UUID
    conversion_factor: float
    stock_primary: float = 0.0
    cost_cpp: float = 0.0


class MaterialUpdate(BaseModel):
    """Esquema para la actualización parcial (PATCH/PUT) de una Materia Prima."""
    name: Optional[str] = None
    primary_unit_id: Optional[uuid.UUID] = None
    secondary_unit_id: Optional[uuid.UUID] = None
    conversion_factor: Optional[float] = None


class MaterialOut(BaseModel):
    """Esquema de salida detallado para Materias Primas."""
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
