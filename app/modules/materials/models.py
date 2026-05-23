"""
===============================================================================
Archivo: models.py
Propósito: Definición de las entidades de base de datos para el módulo de Materias Primas.
Rol Arquitectónico: Entidades de Base de Datos (Entities). Mapean las tablas SQL 
                   usando SQLAlchemy ORM.
===============================================================================
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Supplier(Base):
    """
    Entidad: Proveedores (Suppliers).
    Representa a los proveedores que suministran materias primas a la fábrica.
    """
    __tablename__ = "suppliers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Unit(Base):
    """
    Entidad: Unidades de Medida (Units).
    Define las unidades de compra y uso en la receta (Ej. Kilogramo 'kg', Gramo 'g').
    """
    __tablename__ = "units"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    symbol = Column(String(10), nullable=False)


class RawMaterial(Base):
    """
    Entidad: Materia Prima (Raw Materials).
    El núcleo del módulo. Gestiona el inventario físico y contable de los insumos.
    """
    __tablename__ = "raw_materials"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), index=True, nullable=False)

    # Relaciones de clave foránea hacia la tabla de unidades
    primary_unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    secondary_unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)

    # Factor matemático para convertir de unidad primaria a secundaria. 
    # Ej. Si la unidad primaria es Kg y la secundaria es g, el factor es 1000.
    conversion_factor = Column(Float, nullable=False)  

    # Control de inventario en dos unidades para evitar fracciones complejas en las recetas
    stock_primary = Column(Float, default=0.0)
    stock_secondary = Column(Float, default=0.0)

    # Valoración Contable: Costo Promedio Ponderado (CPP) por unidad primaria
    cost_cpp = Column(Float, default=0.0)  

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relaciones SQLAlchemy para acceder a los objetos Unit directamente (lazy="joined" para mejor rendimiento)
    primary_unit = relationship("Unit", foreign_keys=[primary_unit_id], lazy="joined")
    secondary_unit = relationship("Unit", foreign_keys=[secondary_unit_id], lazy="joined")
