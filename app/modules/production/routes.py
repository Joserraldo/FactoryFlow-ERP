"""
===============================================================================
Archivo: routes.py
Propósito: Endpoints HTTP para la gestión de Órdenes de Producción.
Rol Arquitectónico: Controller. Expone la funcionalidad atómica a través de 
                   la API, garantizando que el usuario esté autenticado.
===============================================================================
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.production.schemas import ProductionOrderCreate, ProductionOrderOut
from app.modules.production.service import ProductionService

router = APIRouter()


@router.post("/", response_model=ProductionOrderOut, status_code=status.HTTP_201_CREATED)
def create_production_order(
    data: ProductionOrderCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Endpoint de grado industrial: Dispara una transacción ACID para construir 
    un lote de productos. 
    Lanza error 400 Bad Request si el inventario de alguna materia prima 
    es insuficiente para cubrir la receta solicitada (BOM).
    """
    return ProductionService(db).create_order(data)


@router.get("/", response_model=List[ProductionOrderOut])
def list_production_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Obtiene el historial (bitácora) de todas las órdenes de producción
    realizadas, incluyendo los operarios asignados y materias primas consumidas.
    """
    return ProductionService(db).list_all(skip, limit)
