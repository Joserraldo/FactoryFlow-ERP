import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.materials.schemas import MaterialCreate, MaterialOut, MaterialUpdate
from app.modules.materials.service import MaterialService

router = APIRouter()


@router.get("/", response_model=List[MaterialOut])
def list_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return MaterialService(db).list_all(skip, limit)


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
