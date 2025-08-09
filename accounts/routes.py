# FastAPI models
from fastapi import APIRouter, status, Response, Depends, Cookie, Request
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
from utils import hash_password, generate_otpcode, validate_password

accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])


# user register route
@accounts_router.post("/register", )
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
    otp = generate_otpcode(new_user.id, response)
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return JSONResponse({'message': 'user is created, now proceed to activate the account'},
                        status_code=status.HTTP_201_CREATED)


# user activation route
@accounts_router.post("/activate", )
async def activate_user(ser: UserActivateSchema, user_id: int = Cookie(None), db: Session = Depends(get_db)):
    """
    with this route the user can activate their account with the otp code sent to them
    """
    print('================================')
    print(user_id)
    print('================================')
    otp_object = db.query(Otp).filter_by(user=user_id).first()
    if otp_object is not None:
        if otp_object.code == ser.code:
            user = db.query(User).filter_by(id=user_id).one_or_none()
            user.is_active = True
            db.delete(otp_object)
            db.commit()
            return JSONResponse({'message': 'user is active'}, status_code=status.HTTP_200_OK)
        return JSONResponse({'message': 'codes doesn\'t match.'}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return JSONResponse({'message': 'no otp codes found'}, status_code=status.HTTP_404_NOT_FOUND)


# get jwt token route
@accounts_router.post("/get_token", )
async def get_token(ser: GetTokenSchema, db: Session = Depends(get_db)):
    """
    with this route the user can get JWT token to authenticate in the app
    """
    is_authenticated = validate_password(db, ser.username, ser.password)
    if is_authenticated:
        jwt_token = generate_jwt_token(ser.username)
        return JSONResponse({'token': jwt_token}, status_code=status.HTTP_200_OK)
    return JSONResponse({'message': 'invalid username or password.'}, status_code=status.HTTP_400_BAD_REQUEST)
