"""
===============================================================================
Archivo: models.py
Propósito: Entidades de Base de Datos para el módulo de Ventas.
Rol Arquitectónico: Define el modelo relacional para clientes, transacciones 
                   (facturas) y los items vendidos.
===============================================================================
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Client(Base):
    """
    Entidad: Cliente (Client).
    Representa a los clientes (B2B o B2C) a los que se les vende el producto terminado.
    """
    __tablename__ = "clients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)


class Sale(Base):
    """
    Entidad: Venta (Sale).
    Equivalente a una Factura o Ticket. Registra la transacción comercial global.
    """
    __tablename__ = "sales"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=False)
    
    # Total monetario de la venta
    total = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relaciones
    client = relationship("Client", lazy="joined")
    # Los detalles de qué productos exactos se vendieron
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    """
    Entidad: Item de Venta (SaleItem).
    Detalle de la factura. Registra el producto específico, cantidad y precio pactado.
    """
    __tablename__ = "sale_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sale_id = Column(String(36), ForeignKey("sales.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    
    # Cantidad vendida y a qué precio unitario se cerró la venta
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)

    # Relaciones
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", lazy="joined")
