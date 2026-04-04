import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.sales.models import Client, Sale


class SalesRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---- Clients ----

    def get_client(self, client_id: uuid.UUID) -> Optional[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def create_client(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def list_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self.db.query(Client).offset(skip).limit(limit).all()

    # ---- Sales ----

    def create_sale(self, sale: Sale) -> Sale:
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def list_sales(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        return self.db.query(Sale).offset(skip).limit(limit).all()
