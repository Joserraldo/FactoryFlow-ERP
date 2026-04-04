"""
FactoryFlow ERP — Database Seeder

Creates:
  - Units (kg, g, L, mL, und)
  - Materials (Harina, Azúcar)
  - Initial Inventory Movements (Stock IN)
  - Products & BOM (Pastel, Pan Dulce)
  - Clients & Sales (Cliente de Prueba)
  - Production Orders
  - Admin user (admin / admin123)

Usage:
  python seed.py
"""
import uuid
import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal, engine
from app.db.base import Base, import_all_models
from app.modules.auth.models import User, UserRole
from app.modules.materials.models import Unit, RawMaterial
from app.modules.products.models import Product, BOMItem
from app.modules.production.models import ProductionOrder, OrderStatus
from app.modules.sales.models import Client, Sale
from app.core.security import get_password_hash

import_all_models()


def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded, if so, wipe tables to ensure fresh seed works without conflict
        if db.query(Unit).first():
            print("✓ Old data detected. Wiping tracking tables to reseed...")
            from sqlalchemy import text
            db.execute(text("TRUNCATE TABLE sales, clients, production_consumptions, production_orders, bom_items, products, inventory_movements, raw_materials, units, refresh_tokens, users CASCADE;"))
            db.commit()

        print("Seeding new database state...")

        # ---- Units ----
        kg = Unit(id=uuid.uuid4(), name="Kilogramo", symbol="kg")
        g = Unit(id=uuid.uuid4(), name="Gramo", symbol="g")
        l = Unit(id=uuid.uuid4(), name="Litro", symbol="L")
        ml = Unit(id=uuid.uuid4(), name="Mililitro", symbol="mL")
        und = Unit(id=uuid.uuid4(), name="Unidad", symbol="und")
        db.add_all([kg, g, l, ml, und])
        db.flush()

        # ---- Raw Materials ----
        harina = RawMaterial(
            id=uuid.uuid4(),
            name="Harina de Trigo",
            primary_unit_id=kg.id,
            secondary_unit_id=g.id,
            conversion_factor=1000.0,
            stock_primary=0.0,
            stock_secondary=0.0,
            cost_cpp=0.0,
        )
        azucar = RawMaterial(
            id=uuid.uuid4(),
            name="Azúcar Refinada",
            primary_unit_id=kg.id,
            secondary_unit_id=g.id,
            conversion_factor=1000.0,
            stock_primary=0.0,
            stock_secondary=0.0,
            cost_cpp=0.0,
        )
        db.add_all([harina, azucar])
        db.flush()

        # ---- Inventory IN Movements (Automatically computes stock/cpp using Service logic) ----
        from app.modules.inventory.service import InventoryService
        from app.modules.inventory.schemas import MovementCreate
        inv_service = InventoryService(db)
        inv_service.create_movement(MovementCreate(
            material_id=harina.id, type="IN", quantity_primary=100.0, unit_cost=15.0
        ))
        inv_service.create_movement(MovementCreate(
            material_id=azucar.id, type="IN", quantity_primary=50.0, unit_cost=20.0
        ))

        # ---- Products & BOM ----
        pastel = Product(id=uuid.uuid4(), name="Pastel de Bodas", sale_price=500.0)
        pan_dulce = Product(id=uuid.uuid4(), name="Pan Dulce Gourmet", sale_price=80.0)
        db.add_all([pastel, pan_dulce])
        db.flush()

        db.add_all([
            BOMItem(id=uuid.uuid4(), product_id=pastel.id, material_id=harina.id, quantity_required=2.5),
            BOMItem(id=uuid.uuid4(), product_id=pastel.id, material_id=azucar.id, quantity_required=1.0),
            BOMItem(id=uuid.uuid4(), product_id=pan_dulce.id, material_id=harina.id, quantity_required=0.5),
            BOMItem(id=uuid.uuid4(), product_id=pan_dulce.id, material_id=azucar.id, quantity_required=0.2),
        ])
        db.flush()

        # ---- Clients & Sales ----
        cliente = Client(id=uuid.uuid4(), name="Pastelería Doña Rosa", email="contacto@donarosa.com")
        db.add(cliente)
        db.flush()

        venta = Sale(id=uuid.uuid4(), client_id=cliente.id, total=1500.0)
        db.add(venta)

        # ---- Production Orders ----
        order = ProductionOrder(id=uuid.uuid4(), product_id=pastel.id, quantity=5, status=OrderStatus.pending)
        db.add(order)

        # ---- Admin User ----
        admin = User(
            id=uuid.uuid4(),
            username="admin",
            email="admin@factoryflow.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.admin,
        )
        db.add(admin)

        db.commit()
        print("✓ All tables seeded successfully! Complete dataset available.")

    except Exception as e:
        db.rollback()
        print(f"✗ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
