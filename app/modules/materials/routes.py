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

class StockAdjustment(BaseModel):
    quantity: float
    unit_cost: float = 0.0

@router.post("/{material_id}/adjust-stock", response_model=MaterialOut)
def adjust_stock(
    material_id: uuid.UUID,
    data: StockAdjustment,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    material = db.query(RawMaterial).filter(RawMaterial.id == str(material_id)).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    # CPP weighted average recalculation (RF-01)
    current_stock = material.stock_primary
    if current_stock + data.quantity > 0:
        material.cost_cpp = (current_stock * material.cost_cpp + data.quantity * data.unit_cost) / (current_stock + data.quantity)
    else:
        material.cost_cpp = data.unit_cost

    material.stock_primary += data.quantity
    if material.conversion_factor:
        material.stock_secondary += (data.quantity * material.conversion_factor)

    db.commit()
    db.refresh(material)
    return material

# ---- Suppliers ----

@router.get("/suppliers", response_model=List[SupplierOut])
def list_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return MaterialService(db).list_suppliers(skip, limit)


@router.post("/suppliers", response_model=SupplierOut, status_code=201)
def create_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return MaterialService(db).create_supplier(data)

# ---- Materials ----

@router.get("/", response_model=List[MaterialOut])
def list_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return MaterialService(db).list_all(skip, limit)

from app.modules.materials.schemas import UnitOut

@router.get("/units", response_model=List[UnitOut])
def list_units(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    from app.modules.materials.models import Unit
    return db.query(Unit).all()


@router.post("/", response_model=MaterialOut, status_code=201)
def create_material(
    data: MaterialCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return MaterialService(db).create(data)


@router.put("/{material_id}", response_model=MaterialOut)
def update_material(
    material_id: uuid.UUID,
    data: MaterialUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return MaterialService(db).update(material_id, data)
