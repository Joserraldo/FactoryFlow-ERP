from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.inventory.schemas import MovementCreate, MovementOut
from app.modules.inventory.service import InventoryService

router = APIRouter()


@router.post("/movement", response_model=MovementOut, status_code=status.HTTP_201_CREATED)
def create_movement(
    data: MovementCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return InventoryService(db).create_movement(data)
