import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.inventory.models import InventoryMovement


class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, movement: InventoryMovement) -> InventoryMovement:
        self.db.add(movement)
        # Commit handled by service (transactional)
        return movement

    def list_by_material(self, material_id: uuid.UUID) -> List[InventoryMovement]:
        return (
            self.db.query(InventoryMovement)
            .filter(InventoryMovement.material_id == material_id)
            .order_by(InventoryMovement.created_at.desc())
            .all()
        )
