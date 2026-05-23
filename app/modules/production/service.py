"""
===============================================================================
Archivo: service.py
Propósito: Lógica de negocio core (El cerebro del sistema ERP).
Rol Arquitectónico: Service Layer. Orquesta la Transaccionalidad ACID (Pilar 3) 
                   y la Trazabilidad Atómica de Producción (Pilar 1).
===============================================================================
"""

import logging
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.inventory.models import InventoryMovement, MovementType
from app.modules.materials.repository import MaterialRepository
from app.modules.production.models import OrderStatus, ProductionConsumption, ProductionOrder, ProductionStep
from app.modules.production.repository import ProductionRepository
from app.modules.production.schemas import ProductionOrderCreate
from app.modules.products.repository import ProductRepository

logger = logging.getLogger(__name__)


class ProductionService:
    """
    Servicio de Dominio encargado de la ejecución y validación de órdenes de manufactura.
    """
    def __init__(self, db: Session):
        """
        Inyecta la sesión global y los 3 repositorios involucrados en una orden:
        Producción, Productos (Receta/BOM) y Materiales (Inventario Físico).
        """
        self.db = db
        self.prod_repo = ProductionRepository(db)
        self.product_repo = ProductRepository(db)
        self.mat_repo = MaterialRepository(db)

    def create_order(self, data: ProductionOrderCreate) -> ProductionOrder:
        """
        Algoritmo Central de Producción (Pilar 1 - Trazabilidad Atómica).
        
        Flujo de Ejecución:
        1. Valida que el producto exista.
        2. Lee el BOM (Receta) y multiplica por el tamaño del lote (quantity).
        3. Valida en Memoria (Phase 1) que TODAS las materias primas tengan stock.
        4. Si hay stock, crea la orden y asigna los operarios a cada paso (Phase 2).
        5. Descuenta el inventario, registra consumo y suma producto terminado (Phase 3).
        6. Guarda TODO en una única transacción ACID. Si la base de datos o el 
           servidor fallan en medio, se hace un Rollback automático y nada se daña.
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
            # =================================================================
            # FASE 1: Validación Previa de Inventario Físico (Fail-Fast)
            # =================================================================
            # Evita crear media orden si falta harina o azúcar para el lote completo.
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

            # =================================================================
            # FASE 2: Estructuración de la Orden y Asignación de Recursos
            # =================================================================
            order = ProductionOrder(
                product_id=str(data.product_id),
                quantity=data.quantity,
                status=OrderStatus.in_progress,
            )
            
            # Mapeo de operarios asignados en el request (Frontend)
            assignment_map = {str(sa.process_id): str(sa.assigned_to) if sa.assigned_to else None for sa in data.step_assignments}
            for process in product.processes:
                step = ProductionStep(
                    process_id=str(process.id),
                    assigned_to=assignment_map.get(str(process.id)),
                    status=OrderStatus.pending
                )
                order.steps.append(step)

            self.prod_repo.create_order(order)

            # =================================================================
            # FASE 3: Deducción Dinámica (OUT) y Construcción
            # =================================================================
            for material, bom, required_qty in material_requirements:
                qty_secondary = required_qty * material.conversion_factor

                # 3.1 Descuento directo en modelo Material (Unidades primarias y secundarias)
                material.stock_primary -= required_qty
                material.stock_secondary -= qty_secondary

                # 3.2 Registro de Movimiento de Inventario (Kardex Contable)
                movement = InventoryMovement(
                    material_id=str(material.id),
                    type=MovementType.OUT,
                    quantity_primary=required_qty,
                    quantity_secondary=qty_secondary,
                    unit_cost=material.cost_cpp, # Asigna el costo promedio actual a la salida
                )
                self.db.add(movement)

                # 3.3 Histórico inmutable de Consumo de esta orden
                consumption = ProductionConsumption(
                    production_order_id=str(order.id),
                    material_id=str(material.id),
                    quantity_used=required_qty,
                    quantity_used_secondary=qty_secondary,
                )
                self.prod_repo.add_consumption(consumption)

            # 3.4 Sumar el Producto Terminado al catálogo listo para venta
            order.status = OrderStatus.completed
            product.current_stock += data.quantity

            # =================================================================
            # PUNTO DE COMMIT ACID (Todo o Nada)
            # =================================================================
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
            self.db.rollback() # Revierte cualquier inserción previa
            raise
        except Exception as e:
            self.db.rollback() # Revierte en caso de un fallo inesperado del servidor o BD
            logger.error("Production order failed: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Production order processing failed",
            )

    def list_all(self, skip: int = 0, limit: int = 100) -> List[ProductionOrder]:
        """Obtiene la bitácora de órdenes generadas."""
        return self.prod_repo.list_all(skip, limit)

    def get(self, order_id: uuid.UUID) -> ProductionOrder:
        """Obtiene el detalle de una orden de producción específica."""
        order = self.prod_repo.get(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production order not found")
        return order
