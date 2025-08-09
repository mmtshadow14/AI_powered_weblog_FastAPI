# FastAPI packages
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Accounts app models
from accounts.routes import accounts_router

# Posts app models
from posts.routes import posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("application startup")
    yield
    print("application shutdown")


app = FastAPI(Lifespan=lifespan)
app.include_router(accounts_router)
app.include_router(posts_router)
