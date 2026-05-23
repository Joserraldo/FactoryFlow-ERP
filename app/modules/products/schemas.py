"""
===============================================================================
Archivo: schemas.py
Propósito: Definición de esquemas de datos (DTOs) usando Pydantic.
Rol Arquitectónico: Data Transfer Objects. Validan la entrada de los items BOM 
                   y la definición del producto antes de llegar a la lógica.
===============================================================================
"""

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, constr


# =============================================================================
# Esquemas de Lista de Materiales (BOM)
# =============================================================================

class BOMItemCreate(BaseModel):
    """Estructura esperada al asociar un ingrediente a una receta."""
    material_id: uuid.UUID
    quantity_required: float


class BOMItemOut(BaseModel):
    """Estructura de respuesta que representa un ingrediente en la receta."""
    id: uuid.UUID
    material_id: uuid.UUID
    quantity_required: float

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Esquemas de Procesos de Manufactura
# =============================================================================

class ProductProcessCreate(BaseModel):
    """Estructura para definir una etapa de producción."""
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    order_index: int = 0


class ProductProcessOut(BaseModel):
    """Estructura de salida para una etapa de producción."""
    id: uuid.UUID
    product_id: uuid.UUID
    name: str
    order_index: int

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Esquemas de Productos
# =============================================================================

class ProductCreate(BaseModel):
    """
    Esquema integral para crear un producto.
    Permite enviar de forma anidada la receta (bom_items) y los procesos.
    """
    name: constr(min_length=1, max_length=100)  # type: ignore[valid-type]
    sale_price: float
    bom_items: List[BOMItemCreate] = []
    processes: List[ProductProcessCreate] = []


class ProductOut(BaseModel):
    """Esquema de salida completo con todas sus relaciones cargadas."""
    id: uuid.UUID
    name: str
    sale_price: float
    current_stock: float
    created_at: datetime
    bom_items: List[BOMItemOut] = []
    processes: List[ProductProcessOut] = []

    model_config = ConfigDict(from_attributes=True)
