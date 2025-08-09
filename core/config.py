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


settings = Settings()

