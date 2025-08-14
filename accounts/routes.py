# Python packages
import random

# FastAPI models
from fastapi import APIRouter, HTTPException, status, Response, Depends, Cookie, Request
from starlette.responses import JSONResponse

# SQLALCHEMY
from sqlalchemy.orm import Session

# APP config
from core.database import get_db

# Accounts app schema
from accounts.schemas import *
from accounts.models import User, Otp

# Authentication models
from auth.auth_token import create_access_token

# Utils
from utils import generate_hash_password, generate_otpcode, verify_password

accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])


# register a new user
@accounts_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserRegisterSchema)
async def register_user(request: UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
    """
    with this route we will create a new user and set and itp code for the user to activate his account and will store
    his account id in his cookie to get it in the activate_user route to understand which account wants to be activated
    """
    is_username_exists = db.query(User).filter_by(username=request.username).one_or_none()
    if is_username_exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='invalid username')
    hashed_password = generate_hash_password(request.password)
    new_user = User(username=request.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    otp = generate_otpcode(new_user.id, response)
    db.add(otp)
    db.commit()
    return new_user


# activate a registered account
@accounts_router.post('/activate', )
async def activate_user(request: UserActivateSchema, user_id: int = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route the user can activate his account, and we will do it with the id that comes from the Cookie that
     we saved it in the register_user route
    """
    otp_obj = db.query(Otp).filter_by(user=user_id).one_or_none()
    if otp_obj and otp_obj.code == request.code:
        user = db.query(User).filter_by(id=user_id).one_or_none()
        user.is_active = True
        db.commit()
        db.refresh(user)
        return JSONResponse({'message': f'{user.username} has been activated successfully'})
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='invalid information')


# get jwt token
@accounts_router.post('/get_token', status_code=status.HTTP_201_CREATED)
async def get_token(request: GetTokenSchema, response: Response, db: Session = Depends(get_db)):
    """
    with this route the user can get a JWT access token if his account be active with sending his username and password
    """
    user = db.query(User).filter_by(username=request.username).one_or_none()
    if user and verify_password(request.password, user.password):
        if user.is_active:
            jwt_token = create_access_token(user.id)
            response.set_cookie(key='jwt_token', value=jwt_token)
            return {'message': 'token is all set now you are able to access to the routes.'}
        return HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='this user is not active')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='we couldn\'t verify you with provided information')
