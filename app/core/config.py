import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FactoryFlow ERP"
    API_V1_STR: str = "/api/v1"

    # JWT
    SECRET_KEY: str = "your_secret_key_from_env"
    REFRESH_SECRET_KEY: str = "your_refresh_secret_key_from_env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/dbname"

    model_config = {"case_sensitive": True, "env_file": ".env", "extra": "ignore"}


settings = Settings()
