# python models
import os

# pydantic models
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/weblog"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "weblog"
    JWT_SECRET_KEY: str = 'jwt-secret-key'
    CELERY_BROKER_URL: str = 'redis://redis:6379/3'
    CELERY_BACKEND_URL: str = 'redis://redis:6379/3'


settings = Settings()

