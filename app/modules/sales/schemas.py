"""
===============================================================================
Archivo: schemas.py
Propósito: Data Transfer Objects (DTOs) para Ventas.
Rol Arquitectónico: Validar que una venta llegue con clientes válidos y 
                   productos con cantidades lógicas (mayores a cero).
===============================================================================
"""

import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, constr


# =============================================================================
# Esquemas de Clientes
# =============================================================================

class ClientCreate(BaseModel):
    """Payload para registrar a un nuevo cliente."""
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    email: Optional[EmailStr] = None


class ClientOut(BaseModel):
    """Esquema de salida para un cliente."""
    id: uuid.UUID
    name: str
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Esquemas de Items de Venta
# =============================================================================

class SaleItemCreate(BaseModel):
    """Detalle de producto y cantidad a vender."""
    product_id: uuid.UUID
    quantity: float
    unit_price: float


class SaleItemOut(BaseModel):
    """Esquema de salida para el detalle de un producto en la factura."""
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: float
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Esquemas de Ventas Globales
# =============================================================================

class SaleCreate(BaseModel):
    """DTO Principal para ejecutar una venta (El cajero)."""
    client_id: uuid.UUID
    items: List[SaleItemCreate]


class SaleOut(BaseModel):
    """Esquema maestro que devuelve la venta (Factura) generada."""
    id: uuid.UUID
    client_id: uuid.UUID
    total: float
    created_at: datetime
    items: List[SaleItemOut]

    model_config = ConfigDict(from_attributes=True)
