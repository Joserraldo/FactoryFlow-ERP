import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base

class Unit(Base):
    __tablename__ = "units"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False) # Kilogramo, Gramo, Litro
    symbol = Column(String, nullable=False) # kg, g, L

class RawMaterial(Base):
    __tablename__ = "raw_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    
    primary_unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)
    secondary_unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)
    
    conversion_factor = Column(Float, nullable=False) # multiplier from primary to secondary (e.g. 1kg -> 1000g)
    
    stock_primary = Column(Float, default=0.0)
    stock_secondary = Column(Float, default=0.0)
    
    cost_cpp = Column(Float, default=0.0) # Costo Promedio Ponderado
    
    created_at = Column(DateTime, default=datetime.utcnow)
