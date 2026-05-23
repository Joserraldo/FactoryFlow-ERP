"""
===============================================================================
Archivo: service.py
Propósito: Lógica de negocio core para Ventas.
Rol Arquitectónico: Service Layer. Orquesta la Transaccionalidad de Venta, 
                   asegurando que el inventario no baje de cero (No Over-selling).
===============================================================================
"""

import logging
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.products.repository import ProductRepository
from app.modules.sales.models import Client, Sale, SaleItem
from app.modules.sales.repository import SalesRepository
from app.modules.sales.schemas import ClientCreate, SaleCreate

logger = logging.getLogger(__name__)


class SalesService:
    """Servicio de Dominio encargado del motor de ventas e inventario terminado."""
    
    def __init__(self, db: Session):
        """
        Inyecta repositorios: Ventas (Para el guardado) y 
        Productos (Para verificación y descuento de stock).
        """
        self.db = db
        self.repo = SalesRepository(db)
        self.product_repo = ProductRepository(db)

    # =========================================================================
    # Lógica de Clientes
    # =========================================================================

    def create_client(self, data: ClientCreate) -> Client:
        """Registra a un cliente."""
        client = Client(name=data.name, email=data.email)
        client = self.repo.create_client(client)
        logger.info("Client created: %s (id=%s)", client.name, client.id)
        return client

    def list_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene la lista de clientes."""
        return self.repo.list_clients(skip, limit)

    # =========================================================================
    # Lógica Transaccional de Ventas
    # =========================================================================

    def create_sale(self, data: SaleCreate) -> Sale:
        """
        Algoritmo de Ejecución de Ventas.
        
        Flujo de Ejecución:
        1. Valida que el cliente exista.
        2. Inicia el ensamblaje de la factura (Total = 0).
        3. Para cada item: 
           - Valida existencia del producto.
           - Valida que haya suficiente stock terminado (Evita inventario negativo).
           - Descuenta el stock en memoria.
           - Agrega el valor al total de la factura.
        4. Verifica que el total de la venta sea positivo.
        5. Aplica un Commit atómico a la base de datos (Persiste todo o falla íntegro).
        """
        client = self.repo.get_client(data.client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        total = 0
        sale = Sale(client_id=str(data.client_id), total=0)
        
        try:
            for item_data in data.items:
                product = self.product_repo.get(item_data.product_id)
                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Product {item_data.product_id} not found"
                    )
                
                # Regla de Negocio Crítica: Prevención de Venta en Descubierto
                if product.current_stock < item_data.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for '{product.name}': available={product.current_stock}, requested={item_data.quantity}"
                    )
                
                # Descuento del stock (Inventario de Producto Terminado)
                product.current_stock -= item_data.quantity
                
                # Registro del item en la factura
                sale_item = SaleItem(
                    product_id=str(item_data.product_id),
                    quantity=item_data.quantity,
                    unit_price=item_data.unit_price
                )
                sale.items.append(sale_item)
                
                # Cálculo Financiero Acumulativo
                total += item_data.quantity * item_data.unit_price

            # Seguro contra ventas en ceros (Regla de negocio extra)
            if total <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sale total must be positive")
            
            sale.total = total
            
            # Commit atómico (El repositorio cierra la transacción aquí)
            sale = self.repo.create_sale(sale)
            logger.info("Sale created: client=%s, total=%.2f", client.name, sale.total)
            return sale
            
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            logger.error("Sale creation failed: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sale processing failed")

    def list_sales(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Obtiene la bitácora de ventas facturadas."""
        return self.repo.list_sales(skip, limit)
