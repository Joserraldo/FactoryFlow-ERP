import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class MovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    material_id = Column(String(36), ForeignKey("raw_materials.id"), nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    quantity_primary = Column(Float, nullable=False)
    quantity_secondary = Column(Float, nullable=False)
    unit_cost = Column(Float, default=0.0)
    supplier_id = Column(String(36), ForeignKey("suppliers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    material = relationship("RawMaterial", lazy="joined")
    supplier = relationship("Supplier", lazy="joined")
