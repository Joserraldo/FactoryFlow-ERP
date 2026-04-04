import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.routes import router as auth_router
from app.modules.materials.routes import router as materials_router
from app.modules.inventory.routes import router as inventory_router
from app.modules.products.routes import router as products_router
from app.modules.production.routes import router as production_router
from app.modules.sales.routes import router as sales_router

# ---- Logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ---- Application ----
app = FastAPI(
    title="FactoryFlow ERP API",
    description="Manufacturing ERP backend — inventory, production, sales",
    version="1.0.0",
)

# CORS — allow all during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Routers ----
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(materials_router, prefix="/materials", tags=["Materials"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(production_router, prefix="/production-orders", tags=["Production"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "FactoryFlow ERP API"}
