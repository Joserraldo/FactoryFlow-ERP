"""
===============================================================================
Archivo: service.py
Propósito: Implementa las reglas y la lógica de negocio del módulo de productos.
Rol Arquitectónico: Service Layer (Casos de uso). Encargado de orquestar 
                   la creación atómica del producto junto con su receta.
===============================================================================
"""

import logging
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.products.models import BOMItem, Product, ProductProcess
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate
from app.modules.materials.repository import MaterialRepository

logger = logging.getLogger(__name__)


class ProductService:
    """Servicio de dominio para Productos."""
    
    def __init__(self, db: Session):
        """
        Inyecta repositorios duales: Products (Para el guardado local) 
        y Materials (Para validar que los ingredientes existen).
        """
        self.repo = ProductRepository(db)
        self.mat_repo = MaterialRepository(db)

    def create(self, data: ProductCreate) -> Product:
        """
        Registra un producto junto con toda su receta (BOM) de forma atómica.
        
        @param data: Esquema anidado del producto, ingredientes y procesos.
        @returns Product: El objeto producto ensamblado y persistido.
        """
        # =====================================================================
        # Regla de Negocio 1: Integridad de la Receta
        # =====================================================================
        # Antes de intentar armar el producto, debemos garantizar que todos
        # los materiales referenciados en el BOM realmente existan en el sistema.
        for item in data.bom_items:
            material = self.mat_repo.get(item.material_id)
            if not material:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Material {item.material_id} not found",
                )

        # Instancia base del producto
        product = Product(name=data.name, sale_price=data.sale_price)

        # =====================================================================
        # Regla de Negocio 2: Ensamblaje en Memoria (Asociación)
        # =====================================================================
        # Agregamos los items de la receta (BOM) a la relación del producto.
        # SQLAlchemy se encargará de inyectar el product_id al guardar.
        for item in data.bom_items:
            bom = BOMItem(
                material_id=str(item.material_id),
                quantity_required=item.quantity_required,
            )
            product.bom_items.append(bom)

        # Agregamos los procesos secuenciales
        for process_data in data.processes:
            process = ProductProcess(
                name=process_data.name,
                order_index=process_data.order_index
            )
            product.processes.append(process)

        # La creación es transaccional, si falla un item, falla todo el producto.
        product = self.repo.create(product)
        logger.info("Product created: %s with %d BOM items, %d processes", product.name, len(product.bom_items), len(product.processes))
        return product

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene catálogo paginado."""
        return self.repo.list_all(skip, limit)

    def get(self, product_id: uuid.UUID) -> Product:
        """Obtiene un producto, lanza error si no es hallado."""
        product = self.repo.get(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product
