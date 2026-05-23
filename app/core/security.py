"""
===============================================================================
Archivo: security.py
Propósito: Funciones criptográficas para hashing de contraseñas y gestión 
           de tokens JWT (JSON Web Tokens).
Rol Arquitectónico: Capa de Seguridad (Security Layer). Aísla la lógica de 
                   encriptación del resto de los servicios de negocio.
Dependencias: jose (JWT), bcrypt (Hashing)
===============================================================================
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import JWTError, jwt
import bcrypt

from app.core.config import settings

logger = logging.getLogger(__name__)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Genera un token de acceso JWT (Access Token) de corta duración.
    
    @param subject: Identificador único del usuario (usualmente el ID de base de datos).
    @param expires_delta: Tiempo de expiración opcional. Si es None, usa el valor por defecto de config.
    @returns str: El token JWT codificado y firmado.
    """
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Genera un token de refresco JWT (Refresh Token) de larga duración.
    
    @param subject: Identificador único del usuario.
    @param expires_delta: Tiempo de expiración opcional. Si es None, usa el valor por defecto de config.
    @returns str: El token JWT de refresco codificado y firmado con su propia clave secreta.
    """
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, *, is_refresh: bool = False) -> dict | None:
    """
    Decodifica y valida matemáticamente la firma de un token JWT.
    
    @param token: El token string a decodificar.
    @param is_refresh: Booleano para saber qué clave secreta usar (Access vs Refresh).
    @returns dict | None: El payload (datos) del token si es válido, o None si expiró/es inválido.
    """
    secret = settings.REFRESH_SECRET_KEY if is_refresh else settings.SECRET_KEY
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        logger.warning("Invalid or expired token presented")
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara una contraseña en texto plano contra su hash almacenado en base de datos.
    
    @param plain_password: La contraseña ingresada por el usuario.
    @param hashed_password: El hash extraído de la base de datos.
    @returns bool: True si coinciden, False en caso contrario.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """
    Aplica una función de derivación de claves (bcrypt) con un 'salt' aleatorio
    para asegurar la contraseña en texto plano.
    
    @param password: La contraseña en texto plano.
    @returns str: El string cifrado (hash) listo para guardar en BD.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
