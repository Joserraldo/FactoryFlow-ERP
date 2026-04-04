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
    return ProductionService(db).create_order(data)


@router.get("/", response_model=List[ProductionOrderOut])
def list_production_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return ProductionService(db).list_all(skip, limit)
