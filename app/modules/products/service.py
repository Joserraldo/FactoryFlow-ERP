import logging
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.products.models import BOMItem, Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate
from app.modules.materials.repository import MaterialRepository

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)
        self.mat_repo = MaterialRepository(db)

    def create(self, data: ProductCreate) -> Product:
        # Validate all BOM materials exist
        for item in data.bom_items:
            material = self.mat_repo.get(item.material_id)
            if not material:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Material {item.material_id} not found",
                )

        product = Product(name=data.name, sale_price=data.sale_price)

        # Build BOM items
        for item in data.bom_items:
            bom = BOMItem(
                material_id=item.material_id,
                quantity_required=item.quantity_required,
            )
            product.bom_items.append(bom)

        product = self.repo.create(product)
        logger.info("Product created: %s with %d BOM items", product.name, len(product.bom_items))
        return product

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.repo.list_all(skip, limit)

    def get(self, product_id: uuid.UUID) -> Product:
        product = self.repo.get(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product
