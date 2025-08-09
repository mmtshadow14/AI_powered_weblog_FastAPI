# Python packages
import random

# FastAPI
from fastapi import Depends, HTTPException, status
from starlette.responses import JSONResponse

# password hash packages
from passlib.hash import bcrypt

# DB
from core.database import get_db
from sqlalchemy.orm import Session

# Account app models
from accounts.models import User, Otp


def hash_password(password):
    return bcrypt.hash(password)


def validate_password(username, password, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).one_or_none()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    password_validation = bcrypt.verify(password, user.password)
    if password_validation:
        return True
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect password')


def create_otp_and_store_in_cookie(response, username, db: Session = Depends(get_db)):
    new_otp = Otp(user=username, otp=random.randint(1000, 9999))
    response.set_cookie(key='otp', value=new_otp.code)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return True
