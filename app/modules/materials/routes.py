from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.modules.materials import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.MaterialOut)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    # Calculate initial secondary stock
    stock_secondary = material.stock_primary * material.conversion_factor
    
    db_material = models.RawMaterial(
        **material.model_dump(),
        stock_secondary=stock_secondary
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.get("/", response_model=List[schemas.MaterialOut])
def read_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.RawMaterial).offset(skip).limit(limit).all()
