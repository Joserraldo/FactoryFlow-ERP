from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.modules.auth.models import User
from app.modules.materials.models import Unit, RawMaterial
import uuid

# Re-import all models to ensure they are registered with Base
from sqlalchemy import inspect

def seed_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if units already exist
    if db.query(Unit).first():
        print("DB already seeded.")
        return

    # Create Units
    kg = Unit(id=uuid.uuid4(), name="Kilogramo", symbol="kg")
    g = Unit(id=uuid.uuid4(), name="Gramo", symbol="g")
    l = Unit(id=uuid.uuid4(), name="Litro", symbol="L")
    ml = Unit(id=uuid.uuid4(), name="Mililitro", symbol="mL")
    und = Unit(id=uuid.uuid4(), name="Unidad", symbol="und")

    db.add_all([kg, g, l, ml, und])
    db.commit()

    # Create a test Material: Harina
    harina = RawMaterial(
        id=uuid.uuid4(),
        name="Harina de Trigo",
        primary_unit_id=kg.id,
        secondary_unit_id=g.id,
        conversion_factor=1000.0,
        stock_primary=50.0,
        stock_secondary=50000.0,
        cost_cpp=1200.0
    )
    
    db.add(harina)
    db.commit()
    
    print("Seed complete! Created basic units and 'Harina de Trigo'.")
    db.close()

if __name__ == "__main__":
    seed_db()
