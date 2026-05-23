"""
===============================================================================
Archivo: session.py
Propósito: Configurar y establecer la conexión con el motor de base de datos.
Rol Arquitectónico: Capa de Infraestructura de Datos. Instancia el motor (Engine)
                   de SQLAlchemy según la URL configurada en las variables de entorno.
===============================================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Crea el motor de conexión a la BD. 
# pool_pre_ping=True verifica si la conexión sigue viva antes de usarla,
# evitando caídas silenciosas de la base de datos (Database Disconnects).
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Fábrica de sesiones (Session Factory). 
# Cada vez que se llama a SessionLocal() en `dependencies.py`, crea un hilo nuevo
# y seguro para realizar consultas transaccionales.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
