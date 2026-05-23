"""
===============================================================================
Archivo: routes.py
Propósito: Definición de los Endpoints HTTP (API REST) para Productos.
Rol Arquitectónico: Controllers / Routers. Interceptan las peticiones HTTP, 
                   inyectan dependencias y delegan al Service Layer.
===============================================================================
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.products.schemas import ProductCreate, ProductOut
from app.modules.products.service import ProductService

router = APIRouter()


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Registra un nuevo Producto Terminado.
    Recibe la estructura del producto junto con el arreglo de su Receta (BOM)
    y sus procesos de manufactura.
    """
    return ProductService(db).create(data)


@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Devuelve el catálogo de productos terminados, incluyendo su stock actual,
    su lista de ingredientes asociados y el precio de venta.
    """
    return ProductService(db).list_all(skip, limit)
