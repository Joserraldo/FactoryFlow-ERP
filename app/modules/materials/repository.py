import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.materials.models import RawMaterial, Unit, Supplier


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---- Units ----

    def get_unit(self, unit_id) -> Optional[Unit]:
        return self.db.query(Unit).filter(Unit.id == str(unit_id)).first()

    def list_units(self) -> List[Unit]:
        return self.db.query(Unit).all()

    # ---- Suppliers ----

    def get_supplier(self, supplier_id) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(Supplier.id == str(supplier_id)).first()

    def list_suppliers(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return self.db.query(Supplier).offset(skip).limit(limit).all()

    def create_supplier(self, supplier: Supplier) -> Supplier:
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    # ---- Materials ----

    def get(self, material_id) -> Optional[RawMaterial]:
        return self.db.query(RawMaterial).filter(RawMaterial.id == str(material_id)).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> List[RawMaterial]:
        return self.db.query(RawMaterial).offset(skip).limit(limit).all()

    def create(self, material: RawMaterial) -> RawMaterial:
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def update(self, material: RawMaterial) -> RawMaterial:
        self.db.commit()
        self.db.refresh(material)
        return material
