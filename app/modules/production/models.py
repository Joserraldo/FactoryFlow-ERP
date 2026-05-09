import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class ProductionOrder(Base):
    __tablename__ = "production_orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    product = relationship("Product", lazy="joined")
    consumptions = relationship("ProductionConsumption", back_populates="production_order", lazy="joined")
    steps = relationship("ProductionStep", back_populates="production_order", cascade="all, delete-orphan", lazy="joined")


class ProductionStep(Base):
    __tablename__ = "production_steps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    production_order_id = Column(String(36), ForeignKey("production_orders.id", ondelete="CASCADE"), nullable=False)
    process_id = Column(String(36), ForeignKey("product_processes.id"), nullable=False)
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)

    # Relationships
    production_order = relationship("ProductionOrder", back_populates="steps")
    process = relationship("ProductProcess", lazy="joined")
    assigned_user = relationship("User", lazy="joined")


class ProductionConsumption(Base):
    __tablename__ = "production_consumptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    production_order_id = Column(
        String(36), ForeignKey("production_orders.id", ondelete="CASCADE"), nullable=False
    )
    material_id = Column(String(36), ForeignKey("raw_materials.id"), nullable=False)
    quantity_used = Column(Float, nullable=False)
    quantity_used_secondary = Column(Float, nullable=True)

    # Relationships
    production_order = relationship("ProductionOrder", back_populates="consumptions")
    material = relationship("RawMaterial", lazy="joined")
