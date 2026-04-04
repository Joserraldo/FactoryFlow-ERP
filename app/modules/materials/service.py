import logging
import uuid
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.materials.models import RawMaterial
from app.modules.materials.repository import MaterialRepository
from app.modules.materials.schemas import MaterialCreate, MaterialUpdate

logger = logging.getLogger(__name__)


class MaterialService:
    def __init__(self, db: Session):
        self.repo = MaterialRepository(db)

    def create(self, data: MaterialCreate) -> RawMaterial:
        # Validate units exist
        if not self.repo.get_unit(data.primary_unit_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Primary unit not found")
        if not self.repo.get_unit(data.secondary_unit_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Secondary unit not found")

        stock_secondary = data.stock_primary * data.conversion_factor

        material = RawMaterial(
            name=data.name,
            primary_unit_id=data.primary_unit_id,
            secondary_unit_id=data.secondary_unit_id,
            conversion_factor=data.conversion_factor,
            stock_primary=data.stock_primary,
            stock_secondary=stock_secondary,
            cost_cpp=data.cost_cpp,
        )
        material = self.repo.create(material)
        logger.info("Material created: %s (id=%s)", material.name, material.id)
        return material

    def list_all(self, skip: int = 0, limit: int = 100) -> List[RawMaterial]:
        return self.repo.list_all(skip, limit)

    def get(self, material_id: uuid.UUID) -> RawMaterial:
        material = self.repo.get(material_id)
        if not material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
        return material

    def update(self, material_id: uuid.UUID, data: MaterialUpdate) -> RawMaterial:
        material = self.get(material_id)

        if data.name is not None:
            material.name = data.name
        if data.primary_unit_id is not None:
            if not self.repo.get_unit(data.primary_unit_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Primary unit not found")
            material.primary_unit_id = data.primary_unit_id
        if data.secondary_unit_id is not None:
            if not self.repo.get_unit(data.secondary_unit_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Secondary unit not found")
            material.secondary_unit_id = data.secondary_unit_id
        if data.conversion_factor is not None:
            material.conversion_factor = data.conversion_factor
            # Recalculate secondary stock
            material.stock_secondary = material.stock_primary * data.conversion_factor

        material = self.repo.update(material)
        logger.info("Material updated: %s", material.id)
        return material
