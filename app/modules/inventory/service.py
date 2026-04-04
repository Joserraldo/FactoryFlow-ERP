import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.inventory.models import InventoryMovement, MovementType
from app.modules.inventory.repository import InventoryRepository
from app.modules.inventory.schemas import MovementCreate
from app.modules.materials.repository import MaterialRepository

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.inv_repo = InventoryRepository(db)
        self.mat_repo = MaterialRepository(db)

    def create_movement(self, data: MovementCreate) -> InventoryMovement:
        """
        Create an inventory movement with full ACID transaction.

        For IN movements:  Recalculate CPP using weighted average cost.
        For OUT movements: Validate sufficient stock, deduct.
        """
        # Validate movement type
        try:
            movement_type = MovementType(data.type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid movement type. Must be 'IN' or 'OUT'",
            )

        if data.quantity_primary <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero",
            )

        # Fetch material
        material = self.mat_repo.get(data.material_id)
        if not material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

        quantity_secondary = data.quantity_primary * material.conversion_factor

        try:
            if movement_type == MovementType.IN:
                self._process_in(material, data.quantity_primary, quantity_secondary, data.unit_cost)
            else:
                self._process_out(material, data.quantity_primary, quantity_secondary)

            movement = InventoryMovement(
                material_id=data.material_id,
                type=movement_type,
                quantity_primary=data.quantity_primary,
                quantity_secondary=quantity_secondary,
                unit_cost=data.unit_cost,
            )
            self.inv_repo.create(movement)

            # Single commit for the entire transaction (movement + stock update)
            self.db.commit()
            self.db.refresh(movement)

            logger.info(
                "Inventory %s: material=%s, qty=%.2f, new_stock=%.2f, cpp=%.4f",
                movement_type.value,
                material.name,
                data.quantity_primary,
                material.stock_primary,
                material.cost_cpp,
            )
            return movement

        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            logger.error("Inventory movement failed: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movement processing failed")

    def _process_in(self, material, qty_primary: float, qty_secondary: float, unit_cost: float) -> None:
        """
        Process an IN movement:
        - Recalculate CPP = (current_stock * current_cpp + new_qty * new_cost) / total_stock
        - Update stock in both units
        """
        current_stock = material.stock_primary
        current_cost = material.cost_cpp

        total_stock = current_stock + qty_primary
        if total_stock > 0:
            material.cost_cpp = (current_stock * current_cost + qty_primary * unit_cost) / total_stock
        else:
            material.cost_cpp = unit_cost

        material.stock_primary = total_stock
        material.stock_secondary = material.stock_secondary + qty_secondary

    def _process_out(self, material, qty_primary: float, qty_secondary: float) -> None:
        """
        Process an OUT movement:
        - Validate stock availability (no negative stock)
        - Deduct from both units
        - CPP remains unchanged on OUT
        """
        if material.stock_primary < qty_primary:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Available: {material.stock_primary:.2f}, requested: {qty_primary:.2f}",
            )

        material.stock_primary -= qty_primary
        material.stock_secondary -= qty_secondary
