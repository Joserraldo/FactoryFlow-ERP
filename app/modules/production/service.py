import logging
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.inventory.models import InventoryMovement, MovementType
from app.modules.materials.repository import MaterialRepository
from app.modules.production.models import OrderStatus, ProductionConsumption, ProductionOrder
from app.modules.production.repository import ProductionRepository
from app.modules.production.schemas import ProductionOrderCreate
from app.modules.products.repository import ProductRepository

logger = logging.getLogger(__name__)


class ProductionService:
    def __init__(self, db: Session):
        self.db = db
        self.prod_repo = ProductionRepository(db)
        self.product_repo = ProductRepository(db)
        self.mat_repo = MaterialRepository(db)

    def create_order(self, data: ProductionOrderCreate) -> ProductionOrder:
        """
        Create a production order:
        1. Validate product exists
        2. Read BOM and calculate required materials
        3. Validate all materials have sufficient stock
        4. Deduct inventory (OUT movements) + record consumptions
        5. All within a single ACID transaction
        """
        product = self.product_repo.get(data.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        bom_items = self.product_repo.get_bom_items(data.product_id)
        if not bom_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product has no BOM items defined",
            )

        try:
            # ---- Phase 1: Validate stock availability ----
            material_requirements = []
            for bom in bom_items:
                required_qty = bom.quantity_required * data.quantity
                material = self.mat_repo.get(bom.material_id)
                if not material:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"BOM references missing material {bom.material_id}",
                    )
                if material.stock_primary < required_qty:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Insufficient stock for '{material.name}': "
                            f"available={material.stock_primary:.2f}, required={required_qty:.2f}"
                        ),
                    )
                material_requirements.append((material, bom, required_qty))

            # ---- Phase 2: Create order ----
            order = ProductionOrder(
                product_id=data.product_id,
                quantity=data.quantity,
                status=OrderStatus.in_progress,
            )
            self.prod_repo.create_order(order)

            # ---- Phase 3: Deduct inventory & record consumptions ----
            for material, bom, required_qty in material_requirements:
                qty_secondary = required_qty * material.conversion_factor

                # Deduct stock
                material.stock_primary -= required_qty
                material.stock_secondary -= qty_secondary

                # Record inventory OUT movement
                movement = InventoryMovement(
                    material_id=material.id,
                    type=MovementType.OUT,
                    quantity_primary=required_qty,
                    quantity_secondary=qty_secondary,
                    unit_cost=material.cost_cpp,
                )
                self.db.add(movement)

                # Record consumption
                consumption = ProductionConsumption(
                    production_order_id=order.id,
                    material_id=material.id,
                    quantity_used=required_qty,
                )
                self.prod_repo.add_consumption(consumption)

            # Mark order completed
            order.status = OrderStatus.completed

            # Single atomic commit
            self.db.commit()
            self.db.refresh(order)

            logger.info(
                "Production order completed: product=%s, qty=%d, materials_consumed=%d",
                product.name,
                data.quantity,
                len(material_requirements),
            )
            return order

        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            logger.error("Production order failed: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Production order processing failed",
            )

    def list_all(self, skip: int = 0, limit: int = 100) -> List[ProductionOrder]:
        return self.prod_repo.list_all(skip, limit)

    def get(self, order_id: uuid.UUID) -> ProductionOrder:
        order = self.prod_repo.get(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production order not found")
        return order
