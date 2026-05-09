import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.production.models import ProductionConsumption, ProductionOrder


class ProductionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, order_id) -> Optional[ProductionOrder]:
        return self.db.query(ProductionOrder).filter(ProductionOrder.id == str(order_id)).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> List[ProductionOrder]:
        return self.db.query(ProductionOrder).offset(skip).limit(limit).all()

    def create_order(self, order: ProductionOrder) -> ProductionOrder:
        self.db.add(order)
        # Commit deferred to service for transactional use
        return order

    def add_consumption(self, consumption: ProductionConsumption) -> ProductionConsumption:
        self.db.add(consumption)
        return consumption
