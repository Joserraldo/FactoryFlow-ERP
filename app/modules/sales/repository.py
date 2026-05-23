"""
===============================================================================
Archivo: repository.py
Propósito: Persistencia y consultas del módulo de Ventas.
Rol Arquitectónico: DAO. Aísla las consultas CRUD de las ventas y clientes.
===============================================================================
"""

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.sales.models import Client, Sale


class SalesRepository:
    """Repositorio de acceso a base de datos para Clientes y Ventas."""
    
    def __init__(self, db: Session):
        self.db = db

    # =========================================================================
    # Operaciones de Clientes (Clients)
    # =========================================================================

    def get_client(self, client_id: uuid.UUID) -> Optional[Client]:
        """Obtiene un cliente por su ID."""
        return self.db.query(Client).filter(Client.id == str(client_id)).first()

    def create_client(self, client: Client) -> Client:
        """Persiste un nuevo cliente."""
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def list_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene la agenda completa de clientes."""
        return self.db.query(Client).offset(skip).limit(limit).all()

    # =========================================================================
    # Operaciones de Ventas (Sales)
    # =========================================================================

    def create_sale(self, sale: Sale) -> Sale:
        """
        Persiste la Venta. Al igual que en Producción, usamos cascade de SQLAlchemy, 
        por lo que guardar el `sale` guarda automáticamente todos sus `items`.
        """
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def list_sales(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Obtiene el historial contable de las ventas."""
        return self.db.query(Sale).offset(skip).limit(limit).all()
