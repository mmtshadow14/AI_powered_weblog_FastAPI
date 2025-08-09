# FastAPI models
from fastapi import APIRouter, status, Response, Depends, Cookie
from starlette.responses import JSONResponse

# SQLALCHEMY
from sqlalchemy.orm import Session

# APP config
from core.database import get_db

# Accounts app schema
from accounts.schemas import *
from accounts.models import *

# Authentication models
from auth.auth_token import generate_jwt_token

# Utils
from utils import hash_password, create_otp_and_store_in_cookie, validate_password

accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])


# user register route
@accounts_router.post("/register",)
async def register_user(ser: UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
    """
    with this route the user can register in the app
    """
    user_existence = db.query(User).filter_by(username=ser.username).one_or_none()
    if user_existence:
        return JSONResponse({'message': 'invalid username'}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    hashed_password = hash_password(ser.password)
    new_user = User(username=ser.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    otp_status = create_otp_and_store_in_cookie(response, new_user.username)
    if otp_status:
        return JSONResponse({'message': 'user is created, now proceed to activate the account'},
                            status_code=status.HTTP_201_CREATED)
    return JSONResponse({'message': 'something went wrong'}, status_code=status.HTTP_412_PRECONDITION_FAILED, )


# user activation route
@accounts_router.post("/activate",)
async def activate_user(ser: UserActivateSchema, username: str = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route the user can activate their account with the otp code sent to them
    """
    otp_object = db.query(Otp).filter_by(username=username).one_or_none()
    if otp_object:
        if otp_object.code == ser.code:
            user = db.query(User).filter_by(username=username).one_or_none()
            user.is_active = True
            db.delete(otp_object)
            db.commit()
            return JSONResponse({'message': 'user is active'}, status_code=status.HTTP_200_OK)
        return JSONResponse({'message': 'codes doesn\'t match.'}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return JSONResponse({'message': 'no otp codes found'}, status_code=status.HTTP_404_NOT_FOUND)


# get jwt token route
@accounts_router.post("/get_token",)
async def get_token(ser: GetTokenSchema):
    """
    with this route the user can get JWT token to authenticate in the app
    """
    is_authenticated = validate_password(ser.username, ser.password)
    if is_authenticated:
        jwt_token = generate_jwt_token(ser.username)
        return JSONResponse({'token': jwt_token}, status_code=status.HTTP_200_OK)
    return JSONResponse({'message': 'invalid username or password.'}, status_code=status.HTTP_400_BAD_REQUEST)





















