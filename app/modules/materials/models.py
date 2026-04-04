import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    symbol = Column(String(10), nullable=False)


class RawMaterial(Base):
    __tablename__ = "raw_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), index=True, nullable=False)

    primary_unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)
    secondary_unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)

    conversion_factor = Column(Float, nullable=False)  # primary → secondary (e.g. 1 kg → 1000 g)

    stock_primary = Column(Float, default=0.0)
    stock_secondary = Column(Float, default=0.0)

    cost_cpp = Column(Float, default=0.0)  # Costo Promedio Ponderado

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    primary_unit = relationship("Unit", foreign_keys=[primary_unit_id], lazy="joined")
    secondary_unit = relationship("Unit", foreign_keys=[secondary_unit_id], lazy="joined")
