import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.products.models import BOMItem, Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, product_id) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == str(product_id)).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_bom_items(self, product_id) -> List[BOMItem]:
        return self.db.query(BOMItem).filter(BOMItem.product_id == str(product_id)).all()
