"""
===============================================================================
Archivo: repository.py
Propósito: Persistencia y consultas de Órdenes de Producción.
Rol Arquitectónico: DAO. Permite realizar operaciones CRUD aisladas del ORM
                   en la capa de servicio superior.
===============================================================================
"""

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.production.models import ProductionConsumption, ProductionOrder


class ProductionRepository:
    """Repositorio de acceso a base de datos para Producción."""
    
    def __init__(self, db: Session):
        self.db = db

    def get(self, order_id: uuid.UUID) -> Optional[ProductionOrder]:
        """Recupera una orden de producción específica."""
        return self.db.query(ProductionOrder).filter(ProductionOrder.id == str(order_id)).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> List[ProductionOrder]:
        """Obtiene la bitácora histórica de todas las órdenes."""
        return self.db.query(ProductionOrder).offset(skip).limit(limit).all()

    def create_order(self, order: ProductionOrder) -> ProductionOrder:
        """
        Registra la orden en la sesión de base de datos.
        NOTA ARQUITECTÓNICA: Se difiere (defer) el db.commit() de manera 
        deliberada para que el Service Layer (Capa de Servicio) pueda incluir 
        esta orden dentro de una transacción ACID más grande (descuentos de stock).
        """
        self.db.add(order)
        # Commit deferred to service for transactional use
        return order

    def add_consumption(self, consumption: ProductionConsumption) -> ProductionConsumption:
        """Añade un registro de consumo a la sesión."""
        self.db.add(consumption)
        return consumption
