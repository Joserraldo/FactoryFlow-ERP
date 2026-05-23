"""
===============================================================================
Archivo: main.py
Propósito: Punto de entrada principal de la aplicación backend FactoryFlow ERP.
Rol Arquitectónico: Actúa como el orquestador principal (Application Root).
                   Configura el servidor FastAPI, inicializa el logging, 
                   configura las políticas CORS y registra todos los enrutadores 
                   (routers) de los distintos módulos de dominio.
Dependencias Clave: 
    - fastapi: Framework principal para construir la API.
    - cors: Middleware para permitir peticiones del frontend.
    - routers: Todos los módulos bajo `app.modules.*.routes`
===============================================================================
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de los enrutadores modulares (Clean Architecture Lite)
from app.modules.auth.routes import router as auth_router
from app.modules.materials.routes import router as materials_router
from app.modules.inventory.routes import router as inventory_router
from app.modules.products.routes import router as products_router
from app.modules.production.routes import router as production_router
from app.modules.sales.routes import router as sales_router

# =============================================================================
# Configuración Global de Logging
# =============================================================================
# Formato estándar para la consola. Es vital para la observabilidad y el 
# debugging en entornos de producción y desarrollo.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# =============================================================================
# Instancia Principal de FastAPI
# =============================================================================
# Se define la instancia de la aplicación con metadatos descriptivos 
# que alimentarán la documentación automática de Swagger (OpenAPI).
app = FastAPI(
    title="FactoryFlow ERP API",
    description="Backend para sistema ERP de Manufactura — Inventario, Producción, Ventas y Costos.",
    version="1.0.0",
)

# =============================================================================
# Configuración de Middlewares (CORS)
# =============================================================================
# Se habilita CORS (Cross-Origin Resource Sharing) para permitir que el 
# Frontend (React/Vite en el puerto 5173) se comunique con esta API sin bloqueos.
# NOTA: En producción estricta, allow_origins debería limitarse a los dominios autorizados.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permitir todos los orígenes en desarrollo
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Permitir todas las cabeceras (Auth, Content-Type, etc.)
)

# =============================================================================
# Registro de Enrutadores (Routers)
# =============================================================================
# Se acoplan las rutas de cada módulo de dominio bajo un prefijo específico.
# Esto mantiene el código desacoplado y la arquitectura monolítica modular.
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(materials_router, prefix="/materials", tags=["Materials"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(production_router, prefix="/production-orders", tags=["Production"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])


@app.get("/", tags=["Health"])
def health_check() -> dict:
    """
    Endpoint de comprobación de salud (Health Check).
    
    Propósito: Verificar que el servidor y la API están levantados y respondiendo.
    Es utilizado habitualmente por balanceadores de carga (Load Balancers) 
    o gestores de contenedores (Docker/Kubernetes) para validar el estado del servicio.
    
    Returns:
        dict: Un diccionario JSON indicando el estado "ok" y el nombre del servicio.
    """
    return {"status": "ok", "service": "FactoryFlow ERP API"}
