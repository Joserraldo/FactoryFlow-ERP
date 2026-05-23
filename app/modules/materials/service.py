"""
===============================================================================
Archivo: service.py
Propósito: Implementa las reglas y la lógica de negocio del módulo de materiales.
Rol Arquitectónico: Service Layer (Casos de uso). Valida reglas de negocio 
                   antes de delegar la persistencia al repositorio.
===============================================================================
"""

import logging
import uuid
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.materials.models import RawMaterial, Supplier
from app.modules.materials.repository import MaterialRepository
from app.modules.materials.schemas import MaterialCreate, MaterialUpdate, SupplierCreate

logger = logging.getLogger(__name__)


class MaterialService:
    """
    Servicio de Lógica de Negocio para Materias Primas y Proveedores.
    """
    def __init__(self, db: Session):
        """Inyecta la sesión de DB e inicializa el repositorio correspondiente."""
        self.repo = MaterialRepository(db)

    # =========================================================================
    # Lógica de Proveedores (Suppliers)
    # =========================================================================
    
    def create_supplier(self, data: SupplierCreate) -> Supplier:
        """
        Crea un nuevo proveedor en el sistema.
        
        @param data: Esquema validado Pydantic con los datos del proveedor.
        @returns Supplier: Entidad del proveedor creada.
        """
        supplier = Supplier(
            name=data.name,
            contact_email=data.contact_email,
            phone=data.phone,
        )
        supplier = self.repo.create_supplier(supplier)
        logger.info("Supplier created: %s (id=%s)", supplier.name, supplier.id)
        return supplier

    def list_suppliers(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        """Obtiene lista paginada de proveedores."""
        return self.repo.list_suppliers(skip, limit)

    def get_supplier(self, supplier_id: uuid.UUID) -> Supplier:
        """
        Obtiene un proveedor, lanza 404 si no existe.
        """
        supplier = self.repo.get_supplier(supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return supplier

    # =========================================================================
    # Lógica de Materias Primas (Materials)
    # =========================================================================
    
    def create(self, data: MaterialCreate) -> RawMaterial:
        """
        Crea una materia prima realizando validaciones de integridad referencial.
        
        @param data: Esquema con los datos iniciales y el factor de conversión.
        @returns RawMaterial: Entidad de la materia prima creada.
        @raises HTTPException 400: Si las unidades primary/secondary no existen.
        """
        # Validación: Asegurar que las unidades foráneas existan en la BD
        if not self.repo.get_unit(data.primary_unit_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Primary unit not found")
        if not self.repo.get_unit(data.secondary_unit_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Secondary unit not found")

        # Regla de Negocio: Calcular automáticamente el stock secundario al crear
        stock_secondary = data.stock_primary * data.conversion_factor

        material = RawMaterial(
            name=data.name,
            primary_unit_id=str(data.primary_unit_id),
            secondary_unit_id=str(data.secondary_unit_id),
            conversion_factor=data.conversion_factor,
            stock_primary=data.stock_primary,
            stock_secondary=stock_secondary,
            cost_cpp=data.cost_cpp,
        )
        material = self.repo.create(material)
        logger.info("Material created: %s (id=%s)", material.name, material.id)
        return material

    def list_all(self, skip: int = 0, limit: int = 100) -> List[RawMaterial]:
        """Obtiene lista paginada de materias primas."""
        return self.repo.list_all(skip, limit)

    def get(self, material_id: uuid.UUID) -> RawMaterial:
        """Obtiene una materia prima, lanza 404 si no existe."""
        material = self.repo.get(material_id)
        if not material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
        return material

    def update(self, material_id: uuid.UUID, data: MaterialUpdate) -> RawMaterial:
        """
        Actualiza parcialmente una materia prima. 
        Recalcula factores de conversión de forma dinámica si este se altera.
        
        @param material_id: ID de la materia prima.
        @param data: Campos opcionales a actualizar.
        @returns RawMaterial: Entidad actualizada.
        """
        material = self.get(material_id)

        if data.name is not None:
            material.name = data.name
            
        if data.primary_unit_id is not None:
            if not self.repo.get_unit(data.primary_unit_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Primary unit not found")
            material.primary_unit_id = str(data.primary_unit_id)
            
        if data.secondary_unit_id is not None:
            if not self.repo.get_unit(data.secondary_unit_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Secondary unit not found")
            material.secondary_unit_id = str(data.secondary_unit_id)
            
        if data.conversion_factor is not None:
            material.conversion_factor = data.conversion_factor
            # Regla de Negocio Crítica: Si cambia el factor de conversión, 
            # el stock secundario debe recalcularse basado en el primario actual.
            material.stock_secondary = material.stock_primary * data.conversion_factor

        material = self.repo.update(material)
        logger.info("Material updated: %s", material.id)
        return material
