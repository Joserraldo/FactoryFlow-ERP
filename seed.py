"""
FactoryFlow ERP — Realistic Database Seeder
Version 1.3 (Demo Ready)
"""
import uuid
import sys
import os
import random
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal, engine
from app.db.base import Base, import_all_models
from app.modules.auth.models import User, UserRole
from app.modules.materials.models import Unit, RawMaterial, Supplier
from app.modules.products.models import Product, BOMItem, ProductProcess
from app.modules.production.models import ProductionOrder, OrderStatus, ProductionStep
from app.modules.sales.models import Client, Sale, SaleItem
from app.core.security import get_password_hash
from app.modules.inventory.service import InventoryService
from app.modules.inventory.schemas import MovementCreate

import_all_models()

def seed_db():
    print("Initializing Realistic Demo Database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ---- Admin User + Workers ----
        admin = User(id=str(uuid.uuid4()), username="admin", email="admin@factoryflow.com", password_hash=get_password_hash("admin123"), role=UserRole.admin)
        operario1 = User(id=str(uuid.uuid4()), username="operario1", email="operario1@factoryflow.com", password_hash=get_password_hash("oper123"), role=UserRole.production)
        operario2 = User(id=str(uuid.uuid4()), username="operario2", email="operario2@factoryflow.com", password_hash=get_password_hash("oper123"), role=UserRole.production)
        operario3 = User(id=str(uuid.uuid4()), username="operario3", email="operario3@factoryflow.com", password_hash=get_password_hash("oper123"), role=UserRole.production)
        db.add_all([admin, operario1, operario2, operario3])
        db.flush()

        # ---- Units ----
        u_kg = Unit(id=str(uuid.uuid4()), name="Kilogramo", symbol="kg")
        u_g = Unit(id=str(uuid.uuid4()), name="Gramo", symbol="g")
        u_l = Unit(id=str(uuid.uuid4()), name="Litro", symbol="L")
        u_ml = Unit(id=str(uuid.uuid4()), name="Mililitro", symbol="mL")
        u_und = Unit(id=str(uuid.uuid4()), name="Unidad", symbol="und")
        db.add_all([u_kg, u_g, u_l, u_ml, u_und])
        db.flush()

        # ---- Suppliers ----
        suppliers = []
        sup_names = ["Molinos El Trigo S.A.", "Lácteos del Valle", "Distribuidora Nacional", "Granjas Avícolas San Juan", "Importaciones Cacao del Sur", "Agricola La Fresa", "Endulzantes Naturales", "Empaques y Logística", "Especias del Mundo", "Levaduras y Fermentos S.A."]
        for name in sup_names:
            s = Supplier(id=str(uuid.uuid4()), name=name, contact_email=f"ventas@{name.split()[0].replace(' ', '').lower()}.com", phone=f"300{random.randint(1000000, 9999999)}")
            suppliers.append(s)
            db.add(s)
        db.flush()

        # ---- Materials ----
        mats_info = [
            ("Harina de Trigo", u_kg, u_g, 1000.0), ("Azúcar Refinada", u_kg, u_g, 1000.0), 
            ("Mantequilla", u_kg, u_g, 1000.0), ("Leche Entera", u_l, u_ml, 1000.0), 
            ("Huevos", u_und, u_und, 1.0), ("Cacao en Polvo", u_kg, u_g, 1000.0), 
            ("Polvo de Hornear", u_kg, u_g, 1000.0), ("Vainilla", u_l, u_ml, 1000.0), 
            ("Sal", u_kg, u_g, 1000.0), ("Levadura Fresca", u_kg, u_g, 1000.0), 
            ("Aceite Vegetal", u_l, u_ml, 1000.0), ("Nueces", u_kg, u_g, 1000.0), 
            ("Almendras", u_kg, u_g, 1000.0), ("Fresas", u_kg, u_g, 1000.0), ("Agua", u_l, u_ml, 1000.0)
        ]
        
        mats = {}
        for name, p_u, s_u, conv in mats_info:
            m = RawMaterial(id=str(uuid.uuid4()), name=name, primary_unit_id=p_u.id, secondary_unit_id=s_u.id, conversion_factor=conv, stock_primary=0.0, stock_secondary=0.0, cost_cpp=0.0)
            mats[name] = m
            db.add(m)
        db.flush()

        # ---- Inventory IN Movements (Massive Supply) ----
        inv_service = InventoryService(db)
        prices = {
            "Harina de Trigo": 3.0, "Azúcar Refinada": 4.5, "Mantequilla": 15.0, "Leche Entera": 4.0,
            "Huevos": 0.5, "Cacao en Polvo": 25.0, "Polvo de Hornear": 10.0, "Vainilla": 40.0,
            "Sal": 1.5, "Levadura Fresca": 8.0, "Aceite Vegetal": 6.0, "Nueces": 45.0, 
            "Almendras": 55.0, "Fresas": 20.0, "Agua": 0.2
        }
        for name, m in mats.items():
            qty = random.uniform(500, 5000)
            cost = prices.get(name, 5.0)
            sup = random.choice(suppliers)
            inv_service.create_movement(MovementCreate(material_id=m.id, type="IN", quantity_primary=qty, unit_cost=cost, supplier_id=sup.id))

        # ---- Exact Recipes for BOM ----
        recipes = {
            "Pastel de Bodas": {
                "price": 120000.0,
                "ingredients": {"Harina de Trigo": 3.5, "Azúcar Refinada": 1.5, "Mantequilla": 1.0, "Leche Entera": 2.0, "Huevos": 12.0, "Polvo de Hornear": 0.05, "Vainilla": 0.1},
                "processes": ["Mezclado", "Horneado", "Enfriado", "Cobertura", "Decoración"]
            },
            "Pan Dulce Gourmet": {
                "price": 8500.0,
                "ingredients": {"Harina de Trigo": 0.5, "Azúcar Refinada": 0.1, "Mantequilla": 0.05, "Leche Entera": 0.2, "Levadura Fresca": 0.02, "Sal": 0.01},
                "processes": ["Amasado", "Fermentación", "Corte", "Horneado"]
            },
            "Galletas de Chispas": {
                "price": 15000.0,
                "ingredients": {"Harina de Trigo": 0.4, "Azúcar Refinada": 0.2, "Mantequilla": 0.25, "Huevos": 2.0, "Cacao en Polvo": 0.1, "Polvo de Hornear": 0.01, "Sal": 0.01},
                "processes": ["Mezcla Seca", "Integración", "Moldeado", "Horneado"]
            },
            "Croissant Francés": {
                "price": 6000.0,
                "ingredients": {"Harina de Trigo": 0.3, "Mantequilla": 0.4, "Leche Entera": 0.1, "Levadura Fresca": 0.01, "Sal": 0.01},
                "processes": ["Amasado", "Hojaldrado Múltiple", "Corte y Enrollado", "Fermentación Larga", "Horneado"]
            },
            "Tarta de Fresa y Almendra": {
                "price": 55000.0,
                "ingredients": {"Harina de Trigo": 0.8, "Mantequilla": 0.4, "Azúcar Refinada": 0.3, "Huevos": 4.0, "Fresas": 1.5, "Almendras": 0.2, "Vainilla": 0.05},
                "processes": ["Preparación Base", "Horneado a Ciegas", "Preparación Crema", "Ensamblaje", "Refrigeración"]
            },
            "Baguette Clásica": {
                "price": 4000.0,
                "ingredients": {"Harina de Trigo": 0.5, "Agua": 0.3, "Levadura Fresca": 0.01, "Sal": 0.01},
                "processes": ["Amasado Autolisis", "Fermentación Principal", "División y Formado", "Horneado con Vapor"]
            }
        }

        products = []
        for p_name, p_data in recipes.items():
            p = Product(id=str(uuid.uuid4()), name=p_name, sale_price=p_data["price"])
            db.add(p)
            db.flush()
            products.append(p)

            # Assign specific exact BOM
            for ing_name, req_qty in p_data["ingredients"].items():
                mat = mats[ing_name]
                db.add(BOMItem(id=str(uuid.uuid4()), product_id=p.id, material_id=mat.id, quantity_required=req_qty))

            # Assign specific Processes
            for i, proc in enumerate(p_data["processes"]):
                db.add(ProductProcess(id=str(uuid.uuid4()), product_id=p.id, name=proc, order_index=i+1))
        
        db.flush()

        # ---- Clients ----
        clients = []
        for i in range(1, 16):
            c = Client(id=str(uuid.uuid4()), name=f"Cliente Empresa {i} S.A.", email=f"empresa{i}@correo.com")
            db.add(c)
            clients.append(c)
        db.flush()

        # ---- Sales ----
        for _ in range(70): # 70 historic sales
            client = random.choice(clients)
            sale = Sale(id=str(uuid.uuid4()), client_id=client.id, total=0)
            db.add(sale)
            db.flush()
            total = 0
            for _ in range(random.randint(1, 4)):
                prod = random.choice(products)
                qty = random.randint(5, 50)
                subtotal = qty * prod.sale_price
                db.add(SaleItem(id=str(uuid.uuid4()), sale_id=sale.id, product_id=prod.id, quantity=qty, unit_price=prod.sale_price))
                total += subtotal
            sale.total = total
        db.flush()

        # ---- Production Orders ----
        for _ in range(40):
            prod = random.choice(products)
            qty = random.randint(10, 200)
            status = random.choice([OrderStatus.pending, OrderStatus.in_progress, OrderStatus.completed])
            po = ProductionOrder(id=str(uuid.uuid4()), product_id=prod.id, quantity=qty, status=status)
            db.add(po)
            db.flush()
            
            # Map processes to steps
            db_procs = db.query(ProductProcess).filter(ProductProcess.product_id == prod.id).order_by(ProductProcess.order_index).all()
            for proc in db_procs:
                step_status = status if status in [OrderStatus.pending, OrderStatus.completed] else random.choice([OrderStatus.completed, OrderStatus.in_progress, OrderStatus.pending])
                db.add(ProductionStep(id=str(uuid.uuid4()), production_order_id=po.id, process_id=proc.id, assigned_to=random.choice([operario1.id, operario2.id, operario3.id]), status=step_status))

        db.commit()
        print("[OK] Massive Realistic Version 1.3 Seed applied!")
        print(f"     - 15 Materials | 10 Suppliers | 6 Exact Recipes | 15 Clients")
        print(f"     - 70 Sales | 40 Production Orders | 4 Users")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seed failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
