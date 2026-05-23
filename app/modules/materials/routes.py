"""
===============================================================================
Archivo: routes.py
Propósito: Definición de los Endpoints HTTP (API REST) para Materias Primas.
Rol Arquitectónico: Controllers / Routers. Interceptan las peticiones HTTP, 
                   inyectan dependencias y delegan al Service Layer.
===============================================================================
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.materials.schemas import MaterialCreate, MaterialOut, MaterialUpdate, SupplierCreate, SupplierOut
from app.modules.materials.service import MaterialService
from app.modules.materials.models import RawMaterial

router = APIRouter()

# =============================================================================
# Esquemas Internos del Router (Solo para Ajustes manuales)
# =============================================================================
class StockAdjustment(BaseModel):
    """Esquema específico para un endpoint de ajuste manual de inventario."""
    quantity: float
    unit_cost: float = 0.0

# =============================================================================
# Ajuste Manual de Stock y Algoritmo de Costo
# =============================================================================
@router.post("/{material_id}/adjust-stock", response_model=MaterialOut)
def adjust_stock(
    material_id: uuid.UUID,
    data: StockAdjustment,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Realiza un ajuste manual de inventario físico sobre una materia prima.
    
    [Lógica Financiera]: Ejecuta el cálculo del Costo Promedio Ponderado (CPP).
    Es vital para mantener la valoración contable correcta tras cada inyección de stock.
    """
    material = db.query(RawMaterial).filter(RawMaterial.id == str(material_id)).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    # -------------------------------------------------------------------------
    # Algoritmo de Recálculo de Costo Promedio Ponderado (CPP) - (RF-01)
    # -------------------------------------------------------------------------
    current_stock = material.stock_primary
    if current_stock + data.quantity > 0:
        # Nuevo CPP = ((Stock Actual * Costo Actual) + (Cantidad Ingresada * Costo Ingreso)) / Nuevo Stock Total
        material.cost_cpp = (current_stock * material.cost_cpp + data.quantity * data.unit_cost) / (current_stock + data.quantity)
    else:
        # Si el inventario estaba en 0 (o menos), asume el costo de la nueva compra
        material.cost_cpp = data.unit_cost

    # Suma algebraica del inventario primario
    material.stock_primary += data.quantity
    
    # Propaga matemáticamente el impacto al inventario secundario
    if material.conversion_factor:
        material.stock_secondary += (data.quantity * material.conversion_factor)

    db.commit()
    db.refresh(material)
    return material

# =============================================================================
# Rutas de Proveedores
# =============================================================================

@router.get("/suppliers", response_model=List[SupplierOut])
def list_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user), # Protegido por JWT
):
    """Obtiene la lista de todos los proveedores."""
    return MaterialService(db).list_suppliers(skip, limit)


@router.post("/suppliers", response_model=SupplierOut, status_code=201)
def create_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Crea un nuevo proveedor en el sistema."""
    return MaterialService(db).create_supplier(data)

# =============================================================================
# Rutas de Materias Primas Principales
# =============================================================================

@router.get("/", response_model=List[MaterialOut])
def list_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Obtiene el listado general de materias primas con su stock y costos."""
    return MaterialService(db).list_all(skip, limit)


from app.modules.materials.schemas import UnitOut

@router.get("/units", response_model=List[UnitOut])
def list_units(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Obtiene el catálogo base de unidades de medida (kg, g, lt, ml, etc)."""
    from app.modules.materials.models import Unit
    return db.query(Unit).all()


@router.post("/", response_model=MaterialOut, status_code=201)
def create_material(
    data: MaterialCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Registra una nueva materia prima y establece su factor de conversión."""
    return MaterialService(db).create(data)


@router.put("/{material_id}", response_model=MaterialOut)
def update_material(
    material_id: uuid.UUID,
    data: MaterialUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Actualiza datos parciales de una materia prima existente."""
    return MaterialService(db).update(material_id, data)
