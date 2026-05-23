"""
===============================================================================
Archivo: models.py
Propósito: Entidades de Base de Datos para el módulo de Producción.
Rol Arquitectónico: Define el modelo relacional para las órdenes de producción,
                   el consumo de materiales y el seguimiento de procesos (steps).
===============================================================================
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    """Enumeración para los estados del ciclo de vida de una orden/paso."""
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class ProductionOrder(Base):
    """
    Entidad: Orden de Producción (ProductionOrder).
    Es el documento central que autoriza la manufactura de un lote de productos.
    """
    __tablename__ = "production_orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    
    # Cantidad de productos a manufacturar en este lote
    quantity = Column(Integer, nullable=False)
    
    # Estado global de la orden
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relaciones
    product = relationship("Product", lazy="joined")
    # consumptions guarda un registro histórico (audit trail) de qué materias primas 
    # exactas se usaron y en qué cantidades para esta orden en particular.
    consumptions = relationship("ProductionConsumption", back_populates="production_order", lazy="joined")
    # steps divide la orden en las fases de manufactura requeridas por el producto
    steps = relationship("ProductionStep", back_populates="production_order", cascade="all, delete-orphan", lazy="joined")


class ProductionStep(Base):
    """
    Entidad: Paso de Producción (ProductionStep).
    Instanciación de un `ProductProcess` atado a una orden específica.
    Permite asignar un trabajador a una tarea específica (ej. Juan hace el Horneado).
    """
    __tablename__ = "production_steps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    production_order_id = Column(String(36), ForeignKey("production_orders.id", ondelete="CASCADE"), nullable=False)
    process_id = Column(String(36), ForeignKey("product_processes.id"), nullable=False)
    
    # Trabajador asignado a esta etapa
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)

    # Relaciones
    production_order = relationship("ProductionOrder", back_populates="steps")
    process = relationship("ProductProcess", lazy="joined")
    assigned_user = relationship("User", lazy="joined")


class ProductionConsumption(Base):
    """
    Entidad: Consumo de Producción (ProductionConsumption).
    Registra de manera inmutable el costo material directo incurrido por una orden.
    """
    __tablename__ = "production_consumptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    production_order_id = Column(
        String(36), ForeignKey("production_orders.id", ondelete="CASCADE"), nullable=False
    )
    material_id = Column(String(36), ForeignKey("raw_materials.id"), nullable=False)
    
    # Cantidad exacta que se dedujo del inventario
    quantity_used = Column(Float, nullable=False)
    quantity_used_secondary = Column(Float, nullable=True)

    # Relaciones
    production_order = relationship("ProductionOrder", back_populates="consumptions")
    material = relationship("RawMaterial", lazy="joined")
