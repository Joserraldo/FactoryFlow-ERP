import logging
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.sales.models import Client, Sale
from app.modules.sales.repository import SalesRepository
from app.modules.sales.schemas import ClientCreate, SaleCreate

logger = logging.getLogger(__name__)


class SalesService:
    def __init__(self, db: Session):
        self.repo = SalesRepository(db)

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

        if data.total <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sale total must be positive")

        sale = Sale(client_id=data.client_id, total=data.total)
        sale = self.repo.create_sale(sale)
        logger.info("Sale created: client=%s, total=%.2f", client.name, sale.total)
        return sale

    def list_sales(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        return self.repo.list_sales(skip, limit)
