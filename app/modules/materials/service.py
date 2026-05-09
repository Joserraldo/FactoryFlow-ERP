import logging
import uuid
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.materials.models import RawMaterial, Supplier
from app.modules.materials.repository import MaterialRepository
from app.modules.materials.schemas import MaterialCreate, MaterialUpdate, SupplierCreate

logger = logging.getLogger(__name__)


class MaterialService:
    def __init__(self, db: Session):
        self.repo = MaterialRepository(db)

    # ---- Suppliers ----
    def create_supplier(self, data: SupplierCreate) -> Supplier:
        supplier = Supplier(
            name=data.name,
            contact_email=data.contact_email,
            phone=data.phone,
        )
        supplier = self.repo.create_supplier(supplier)
        logger.info("Supplier created: %s (id=%s)", supplier.name, supplier.id)
        return supplier

    def list_suppliers(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return self.repo.list_suppliers(skip, limit)

    def get_supplier(self, supplier_id: uuid.UUID) -> Supplier:
        supplier = self.repo.get_supplier(supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return supplier

    # ---- Materials ----
    def create(self, data: MaterialCreate) -> RawMaterial:
        # Validate units exist
        if not self.repo.get_unit(data.primary_unit_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Primary unit not found")
        if not self.repo.get_unit(data.secondary_unit_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Secondary unit not found")

        stock_secondary = data.stock_primary * data.conversion_factor

        material = RawMaterial(
            name=data.name,
            primary_unit_id=str(data.primary_unit_id),
            secondary_unit_id=str(data.secondary_unit_id),
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
            material.primary_unit_id = str(data.primary_unit_id)
        if data.secondary_unit_id is not None:
            if not self.repo.get_unit(data.secondary_unit_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Secondary unit not found")
            material.secondary_unit_id = str(data.secondary_unit_id)
        if data.conversion_factor is not None:
            material.conversion_factor = data.conversion_factor
            # Recalculate secondary stock
            material.stock_secondary = material.stock_primary * data.conversion_factor

        material = self.repo.update(material)
        logger.info("Material updated: %s", material.id)
        return material
