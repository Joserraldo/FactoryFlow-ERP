from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.materials.routes import router as materials_router

app = FastAPI(title="FactoryFlow ERP API")

# Add CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(materials_router, prefix="/materials", tags=["materials"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FactoryFlow ERP API"}
