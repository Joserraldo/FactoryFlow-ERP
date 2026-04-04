import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.materials.models import RawMaterial, Unit


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---- Units ----

    def get_unit(self, unit_id: uuid.UUID) -> Optional[Unit]:
        return self.db.query(Unit).filter(Unit.id == unit_id).first()

    def list_units(self) -> List[Unit]:
        return self.db.query(Unit).all()

    # ---- Materials ----

    def get(self, material_id: uuid.UUID) -> Optional[RawMaterial]:
        return self.db.query(RawMaterial).filter(RawMaterial.id == material_id).first()

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
