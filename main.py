from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("application startup")
    yield
    print("application shutdown")


app = FastAPI(Lifespan=lifespan)