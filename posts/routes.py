# FastAPI models
from fastapi import APIRouter
from starlette.responses import JSONResponse

posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.get('all_posts/', )
async def get_all_posts():
    return JSONResponse({'message': 'COMING SOON!!!'})
