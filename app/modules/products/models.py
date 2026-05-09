import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, index=True)
    sale_price = Column(Float, nullable=False)
    current_stock = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    bom_items = relationship("BOMItem", back_populates="product", lazy="joined")
    processes = relationship("ProductProcess", back_populates="product", order_by="ProductProcess.order_index", cascade="all, delete-orphan", lazy="joined")


class ProductProcess(Base):
    __tablename__ = "product_processes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    order_index = Column(Integer, default=0, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="processes")


class BOMItem(Base):
    __tablename__ = "bom_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    material_id = Column(String(36), ForeignKey("raw_materials.id"), nullable=False)
    quantity_required = Column(Float, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="bom_items")
    material = relationship("RawMaterial", lazy="joined")
