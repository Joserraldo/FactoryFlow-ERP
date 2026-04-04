from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.sales.schemas import ClientCreate, ClientOut, SaleCreate, SaleOut
from app.modules.sales.service import SalesService

router = APIRouter()


# ---- Clients ----

@router.post("/clients", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(
    data: ClientCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return SalesService(db).create_client(data)


@router.get("/clients", response_model=List[ClientOut])
def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return SalesService(db).list_clients(skip, limit)


# ---- Sales ----

@router.post("/", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return SalesService(db).create_sale(data)


@router.get("/", response_model=List[SaleOut])
def list_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return SalesService(db).list_sales(skip, limit)
