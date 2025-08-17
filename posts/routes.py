# FastAPI models
from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from starlette.responses import JSONResponse
from typing import List

# SQLALCHEMY
from sqlalchemy.orm import Session

# database
from core.database import get_db

# JWT
from auth.auth_token import retrieve_user_via_jwt

# Posts App Models
from posts.models import Post

# Posts App Schemas
from posts.schemas import create_post_schemas, get_post_schemas

# AI
from AI.ai_funcs import get_keywords

posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.get('/all', status_code=status.HTTP_200_OK, response_model=List[get_post_schemas])
async def get_all_posts(jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.active:
        posts = db.query(Post).all()
        return posts
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')


@posts_router.post('/create', )
async def create_post(ser: create_post_schemas, jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_active:
        keywords = get_keywords(ser.description)
        new_post = Post(user=user.id, title=ser.title, description=ser.description, tags=keywords)
        print('============================')
        print(new_post.tags)
        print('============================')
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return JSONResponse({'message': 'post created successfully.'})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')
