# FastAPI models
from fastapi import APIRouter, Cookie, Depends
from starlette.responses import JSONResponse

# SQLALCHEMY
from sqlalchemy.orm import Session

# database
from core.database import get_db

# JWT
from auth.auth_token import retrieve_user_via_jwt

# Posts App Models
from posts.models import Post

# Posts App Schemas
from posts.schemas import create_post_schemas

posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.get('/all', )
async def get_all_posts(jwt_token: str = Cookie(None)):
    user = retrieve_user_via_jwt(jwt_token)
    return JSONResponse({'username': f'{user.username}',
                         'user_id': f'{user.id}'})


@posts_router.post('/create', )
async def create_post(ser: create_post_schemas, db: Session = Depends(get_db)):
    pass
