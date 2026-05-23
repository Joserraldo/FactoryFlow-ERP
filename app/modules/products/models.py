"""
===============================================================================
Archivo: models.py
Propósito: Definición de las entidades relacionadas a Productos y Recetas (BOM).
Rol Arquitectónico: Entidades de Base de Datos (Entities). Define cómo se 
                   almacena un producto final y sus dependencias de manufactura.
===============================================================================
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    """
    Entidad: Producto (Product).
    Representa un artículo terminado, listo para la venta.
    """
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, index=True)
    sale_price = Column(Float, nullable=False)
    
    # El stock de productos terminados aumenta al completar órdenes de producción
    # y disminuye al registrar ventas.
    current_stock = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relaciones de agregación
    # Un producto está compuesto por una lista de materiales (Receta)
    bom_items = relationship("BOMItem", back_populates="product", lazy="joined")
    # Un producto pasa por varios procesos de manufactura
    processes = relationship("ProductProcess", back_populates="product", order_by="ProductProcess.order_index", cascade="all, delete-orphan", lazy="joined")


class ProductProcess(Base):
    """
    Entidad: Proceso de Producto (ProductProcess).
    Define las etapas (rutas) de manufactura requeridas para ensamblar/cocinar el producto.
    Ej: 1. Mezclado, 2. Horneado, 3. Empaquetado.
    """
    __tablename__ = "product_processes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    order_index = Column(Integer, default=0, nullable=False)  # Orden secuencial del proceso

    # Relación inversa al producto padre
    product = relationship("Product", back_populates="processes")


class BOMItem(Base):
    """
    Entidad: Item de Lista de Materiales (BOMItem - Bill Of Materials).
    Es la tabla intermedia que asocia un Producto Terminado con las Materias 
    Primas necesarias para producir 1 unidad (Receta).
    """
    __tablename__ = "bom_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    material_id = Column(String(36), ForeignKey("raw_materials.id"), nullable=False)
    
    # Cantidad requerida de materia prima (en su unidad primaria) para fabricar 1 producto
    quantity_required = Column(Float, nullable=False)

    # Relaciones
    product = relationship("Product", back_populates="bom_items")
    # lazy="joined" permite cargar el material al vuelo sin queries adicionales N+1
    material = relationship("RawMaterial", lazy="joined")
