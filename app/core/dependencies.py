"""
===============================================================================
Archivo: dependencies.py
Propósito: Inyección de dependencias (Dependency Injection) centralizada para FastAPI.
Rol Arquitectónico: Provee recursos compartidos a las rutas de forma desacoplada, 
                   como sesiones de base de datos y la identidad del usuario autenticado.
===============================================================================
"""

import logging
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

# Definición del esquema de seguridad de FastAPI. Extraerá automáticamente
# el token del header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> Generator:
    """
    Inyector de Sesión de Base de Datos (Database Session Yielder).
    
    Abre una conexión a la BD, la entrega (yield) a la petición en curso 
    y garantiza que se cierre correctamente al finalizar, evitando fugas de memoria.
    
    @returns Generator: Objeto de sesión de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Middleware de Autenticación de Usuario.
    
    Interviene en las rutas protegidas, toma el token JWT extraído por `oauth2_scheme`,
    lo decodifica y busca al usuario en la BD. Si falla en cualquier punto, 
    lanza un error HTTP 401.
    
    @param token: Token JWT inyectado automáticamente.
    @param db: Sesión de BD inyectada automáticamente.
    @returns User: El objeto modelo del Usuario actual (Autenticado).
    @raises HTTPException: 401 si el token es inválido o el usuario no existe.
    """
    # Importación tardía (late import) para evitar problemas de dependencias circulares
    # al cargar los modelos.
    from app.modules.auth.models import User  

    payload = decode_token(token, is_refresh=False)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # El 'sub' del JWT guarda el ID del usuario
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # Busca físicamente en la BD si el ID del token corresponde a un usuario vivo
    user = db.query(User).filter(User.id == str(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    logger.debug("Authenticated user: %s", user.username)
    return user
