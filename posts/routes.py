# FastAPI models
from fastapi import APIRouter, Cookie
from starlette.responses import JSONResponse

# JWT
from auth.auth_token import retrieve_user_via_jwt

posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.get('/all_posts', )
async def get_all_posts(jwt_token: str = Cookie(None)):
    user = retrieve_user_via_jwt(jwt_token)
    return JSONResponse({'username': f'{user.username}',
                         'user_id': f'{user.id}'})
