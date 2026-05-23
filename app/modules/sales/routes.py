"""
===============================================================================
Archivo: routes.py
Propósito: Endpoints HTTP (API REST) para Ventas y Clientes.
Rol Arquitectónico: Controller. Expone la funcionalidad protegiéndola con 
                   Autenticación JWT.
===============================================================================
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.sales.schemas import ClientCreate, ClientOut, SaleCreate, SaleOut
from app.modules.sales.service import SalesService

router = APIRouter()


# =============================================================================
# Rutas de Clientes
# =============================================================================

@router.post("/clients", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(
    data: ClientCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Registra a un nuevo cliente en el directorio."""
    return SalesService(db).create_client(data)


@router.get("/clients", response_model=List[ClientOut])
def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Devuelve el directorio completo de clientes registrados."""
    return SalesService(db).list_clients(skip, limit)


# =============================================================================
# Rutas de Ventas (Punto de Venta)
# =============================================================================

@router.post("/", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Registra una Factura de Venta de manera Atómica.
    Descuenta del inventario final los productos que se están comprando.
    Si un producto no tiene suficiente stock, se aborta la venta completa (Rollback).
    """
    return SalesService(db).create_sale(data)


@router.get("/", response_model=List[SaleOut])
def list_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Obtiene el historial de todas las transacciones de ventas cerradas."""
    return SalesService(db).list_sales(skip, limit)
