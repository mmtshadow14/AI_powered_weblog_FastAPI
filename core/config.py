# python models
import os

# pydantic models
from pydantic import BaseSettings

# DATABASE_URL = os.getenv("DATABASE_URL")


class Settings(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://postgres:psotgres@localhost:5432/weblog"
    JWT_SECRET_KEY: str = 'jwt-secret-key'


settings = Settings()

