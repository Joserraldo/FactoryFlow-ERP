"""
===============================================================================
Archivo: repository.py
Propósito: Abstracción del acceso a datos para Productos y sus Recetas (BOM).
Rol Arquitectónico: Data Access Object (DAO) / Repository Pattern. Aisla 
                   las consultas complejas de orquestación de productos.
===============================================================================
"""

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.products.models import BOMItem, Product


class ProductRepository:
    """
    Repositorio centralizado para operaciones de lectura/escritura de productos.
    """
    def __init__(self, db: Session):
        self.db = db

    def get(self, product_id: uuid.UUID) -> Optional[Product]:
        """Obtiene un producto específico por su ID."""
        return self.db.query(Product).filter(Product.id == str(product_id)).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene una lista paginada del catálogo de productos."""
        return self.db.query(Product).offset(skip).limit(limit).all()

    def create(self, product: Product) -> Product:
        """
        Persiste un nuevo producto en la base de datos.
        NOTA: Gracias a SQLAlchemy (cascade rule), al guardar este producto 
        se guardarán automáticamente todos sus 'bom_items' y 'processes' anidados.
        """
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_bom_items(self, product_id: uuid.UUID) -> List[BOMItem]:
        """Obtiene la lista de materiales (receta) para un producto específico."""
        return self.db.query(BOMItem).filter(BOMItem.product_id == str(product_id)).all()
