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
    def __init__(self, db: Session):
        self.db = db
        self.repo = SalesRepository(db)
        self.product_repo = ProductRepository(db)

    # ---- Clients ----

    def create_client(self, data: ClientCreate) -> Client:
        client = Client(name=data.name, email=data.email)
        client = self.repo.create_client(client)
        logger.info("Client created: %s (id=%s)", client.name, client.id)
        return client

    def list_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self.repo.list_clients(skip, limit)

    # ---- Sales ----

    def create_sale(self, data: SaleCreate) -> Sale:
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
                
                if product.current_stock < item_data.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for '{product.name}': available={product.current_stock}, requested={item_data.quantity}"
                    )
                
                # Deduct stock
                product.current_stock -= item_data.quantity
                
                sale_item = SaleItem(
                    product_id=str(item_data.product_id),
                    quantity=item_data.quantity,
                    unit_price=item_data.unit_price
                )
                sale.items.append(sale_item)
                total += item_data.quantity * item_data.unit_price

            if total <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sale total must be positive")
            
            sale.total = total
            
            # The repository commit will finalize everything
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
        return self.repo.list_sales(skip, limit)
