from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FactoryFlow ERP"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey_change_me_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    DATABASE_URL: str = "sqlite:///./factoryflow.db"

    class Config:
        case_sensitive = True

settings = Settings()
