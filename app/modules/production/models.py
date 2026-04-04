import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class ProductionOrder(Base):
    __tablename__ = "production_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    product = relationship("Product", lazy="joined")
    consumptions = relationship("ProductionConsumption", back_populates="production_order", lazy="joined")


class ProductionConsumption(Base):
    __tablename__ = "production_consumptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    production_order_id = Column(
        UUID(as_uuid=True), ForeignKey("production_orders.id", ondelete="CASCADE"), nullable=False
    )
    material_id = Column(UUID(as_uuid=True), ForeignKey("raw_materials.id"), nullable=False)
    quantity_used = Column(Float, nullable=False)

    # Relationships
    production_order = relationship("ProductionOrder", back_populates="consumptions")
    material = relationship("RawMaterial", lazy="joined")
