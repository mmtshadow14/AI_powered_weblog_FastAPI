# FastAPI packages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

# Accounts app models
from accounts.routes import accounts_router

# Posts app models
from posts.routes import posts_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("application startup")
    yield
    print("application shutdown")


app = FastAPI(Lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,  # This is crucial for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(accounts_router)
app.include_router(posts_router)
