# FastAPI models
from fastapi import APIRouter, status, Response, Depends
from starlette.responses import JSONResponse

# SQLALCHEMY
from sqlalchemy.orm import Session

# APP config
from core.database import get_db

# Accounts app schema
from accounts.schemas import *
from accounts.models import *

# Utils
from utils import hash_password, create_otp_and_store_in_cookie

accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])


@accounts_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(ser: UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
    user_existence = db.query(User).filter_by(username=ser.username).one_or_none()
    if user_existence:
        return JSONResponse({'message': 'invalid username'}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    hashed_password = hash_password(ser.password)
    new_user = User(username=ser.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    create_otp_and_store_in_cookie(response, new_user.username)
    return JSONResponse({'message': 'user is created, now proceed to activate the account'}, status_code=status.HTTP_201_CREATED)

