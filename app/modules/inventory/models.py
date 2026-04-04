import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class MovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    material_id = Column(UUID(as_uuid=True), ForeignKey("raw_materials.id"), nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    quantity_primary = Column(Float, nullable=False)
    quantity_secondary = Column(Float, nullable=False)
    unit_cost = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    material = relationship("RawMaterial", lazy="joined")
