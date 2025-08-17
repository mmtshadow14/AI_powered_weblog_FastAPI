# Python Packages
import json

# FastAPI models
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from starlette.responses import JSONResponse
from typing import List, Optional

# SQLALCHEMY
from sqlalchemy.orm import Session

# database
from core.database import get_db

# JWT
from auth.auth_token import retrieve_user_via_jwt

# Posts App Models
from posts.models import Post, Like

# Posts App Schemas
from posts.schemas import create_post_schemas, get_post_schemas

# AI
from AI.ai_funcs import get_keywords

# utils
from utils import check_like_status

posts_router = APIRouter(prefix="/posts", tags=["posts"])


# get all posts
@posts_router.get('/all', status_code=status.HTTP_200_OK, response_model=List[get_post_schemas])
async def get_all_posts(jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route we will get all posts and show it to the user.
    """
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.active:
        posts = db.query(Post).all()
        return posts
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')


# create post
@posts_router.post('/create', )
async def create_post(ser: create_post_schemas, jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route the user can create a new post and with sending the description to the AI, AI will return its
    keywords to us, so we can store them in the database and, we can use the key word to recognize what post is about
    and show it to the user or not.
    """
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


# get post with ID
@posts_router.get('/get_post/{post_id}', status_code=status.HTTP_200_OK, response_model=[get_post_schemas])
async def get_post_by_id(post_id: int, jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route we will get a post from the ID that user sends and if it exists, we will show it to the user.
    """
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_active:
        post = db.query(Post).filter_by(id=post_id).one_or_none()
        if post:
            return post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')


@posts_router.get('/like_post/{post_id}', )
async def like_post(post_id: int, response: Response, jwt_token: str = Cookie(None), liked: Optional[str] = Cookie(default="[]"), db: Session = Depends(get_db)):
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_active:
        post = db.query(Post).filter_by(id=post_id).one_or_none()
        if post:
            like_status = check_like_status(user.id, post.id)
            if like_status is not False:
                db.delete(like_status)
                db.commit()
                return JSONResponse({'message': 'your like is removed successfully.'})
            new_like_relation = Like(user=user.id, post_id=post.id)
            liked_tags = json.loads(liked)
            updated_tags = list(set(liked_tags + post.tags))
            response.set_cookie(key="liked", value=json.dumps(updated_tags))
            db.add(new_like_relation)
            db.commit()
            return JSONResponse({'message': 'your liked this post successfully.'})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')























