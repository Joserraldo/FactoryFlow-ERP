"""
===============================================================================
Archivo: repository.py
Propósito: Abstracción del acceso a datos para el módulo de materiales.
Rol Arquitectónico: Data Access Object (DAO) / Repository Pattern. Aisla 
                   las consultas SQL del resto de la lógica de negocio.
===============================================================================
"""

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.materials.models import RawMaterial, Unit, Supplier


class MaterialRepository:
    """
    Repositorio para gestionar operaciones de base de datos relacionadas 
    con Unidades, Proveedores y Materias Primas.
    """
    def __init__(self, db: Session):
        """
        Inicializa el repositorio.
        @param db: Instancia de la sesión de base de datos activa.
        """
        self.db = db

    # =========================================================================
    # Operaciones de Unidades (Units)
    # =========================================================================

    def get_unit(self, unit_id: uuid.UUID) -> Optional[Unit]:
        """Obtiene una unidad por su ID."""
        return self.db.query(Unit).filter(Unit.id == str(unit_id)).first()

    def list_units(self) -> List[Unit]:
        """Obtiene el catálogo completo de unidades."""
        return self.db.query(Unit).all()

    # =========================================================================
    # Operaciones de Proveedores (Suppliers)
    # =========================================================================

    def get_supplier(self, supplier_id: uuid.UUID) -> Optional[Supplier]:
        """Obtiene un proveedor por su ID."""
        return self.db.query(Supplier).filter(Supplier.id == str(supplier_id)).first()

    def list_suppliers(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        """Obtiene la lista paginada de proveedores."""
        return self.db.query(Supplier).offset(skip).limit(limit).all()

    def create_supplier(self, supplier: Supplier) -> Supplier:
        """Persiste un nuevo proveedor en la base de datos."""
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier) # Recarga el objeto para obtener su ID autogenerado
        return supplier

    # =========================================================================
    # Operaciones de Materias Primas (Materials)
    # =========================================================================

    def get(self, material_id: uuid.UUID) -> Optional[RawMaterial]:
        """Obtiene una materia prima específica."""
        return self.db.query(RawMaterial).filter(RawMaterial.id == str(material_id)).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> List[RawMaterial]:
        """Obtiene la lista paginada de materias primas."""
        return self.db.query(RawMaterial).offset(skip).limit(limit).all()

    def create(self, material: RawMaterial) -> RawMaterial:
        """Persiste una nueva materia prima."""
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def update(self, material: RawMaterial) -> RawMaterial:
        """Guarda los cambios de una materia prima existente."""
        self.db.commit()
        self.db.refresh(material)
        return material
