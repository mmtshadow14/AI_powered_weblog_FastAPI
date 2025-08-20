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
async def get_all_posts(jwt_token: str = Cookie(None), liked: Optional[str] = Cookie(default="[]"),
                        db: Session = Depends(get_db)):
    """
    with this route we will get all posts that are in commen with the users interests and returns it to the user
    """
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_active:
        posts = db.query(Post).all()
        liked_tags = json.loads(liked)
        if not liked_tags:
            return posts
        recommended_post_list_id = []
        for post in posts:
            tags_in_commen = len(set(post.tags) & set(liked_tags))
            if tags_in_commen > 0:
                recommended_post_list_id.append(post.id)
        filtered_posts = [post for post in posts if post.id in recommended_post_list_id]
        return filtered_posts
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
@posts_router.get('/get_post/{post_id}', status_code=status.HTTP_200_OK, response_model=get_post_schemas)
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


# like post route
@posts_router.get('/like_post/{post_id}', )
async def like_post(post_id: int, response: Response, jwt_token: str = Cookie(None),
                    liked: Optional[str] = Cookie(default="[]"), db: Session = Depends(get_db)):
    """
    with this route the user can like a post and with this we will understand the user's interests and store
    the post tags in his cookie and his user obj to recommend posts which meets his interests.
    """
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_active:
        post = db.query(Post).filter_by(id=post_id).one_or_none()
        if post:
            like_status = check_like_status(user.id, post.id)
            if like_status is not False:
                db.delete(like_status)
                db.commit()
                post.likes -= 1
                return JSONResponse({'message': 'your like is removed successfully.'})
            new_like_relation = Like(user=user.id, post_id=post.id)
            liked_tags = json.loads(liked)
            updated_tags = list(set(liked_tags + post.tags))
            user.liked_tages.append(post.tags)
            response.set_cookie(key="liked", value=json.dumps(updated_tags))
            for tag in post.tags:
                user.liked_tags.append(tag)
            post.likes += 1
            db.add(new_like_relation)
            db.commit()
            db.refresh(user)
            return JSONResponse({'message': 'your liked this post successfully.'})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')


# get all user's posts
@posts_router.get('/my_posts', status_code=status.HTTP_200_OK, response_model=List[get_post_schemas])
async def get_all_user_posts(jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route user can get all the posts he posted.
    """
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_active:
        user_posts = db.query(Post).filter_by(user=user.id).all()
        if user_posts:
            return user_posts
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='you haven\'t post anything yet.')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')


# delete post route
@posts_router.delete('/delete_post/{post_id}',)
async def delete_post(post_id: int, jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route the user can delete the posts that he owns.
    """
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_actie:
        post = db.query(Post).filter_by(id=post_id).one_or_none()
        if post:
            if post.user == user.id:
                db.delete(post)
                db.commit()
                return JSONResponse({'massage': 'post deleted successfully.'})
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you are not the owner of the post.')
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no post found.')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')


# update post route
@posts_router.put('/update_post/{post_id}',)
async def update_post(post_id: int, ser: create_post_schemas, jwt_token: str = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route user can update the posts he owns and if any changes needs to be done with the tags of the post
    the description will be sent to AI and the AI will generate the new keywords, and we will store the tags in the
    post object again.
    """
    user = retrieve_user_via_jwt(jwt_token)
    if user and user.is_active:
        post = db.query(Post).filter_by(id=post_id).one_or_none()
        if post:
            if post.user == user.id:
                keywords = get_keywords(ser.description)
                post.title = ser.title
                post.description = ser.description
                post.tags = keywords
                db.commit()
                db.refresh(post)
                return JSONResponse({'massage': 'post updated successfully.'})
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you are not the owner of the post.')
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no post found.')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')












