# Python packages
import random

# FastAPI
from fastapi import Depends, HTTPException, status
from starlette.responses import JSONResponse

# password hash packages
from passlib.hash import bcrypt

# DB
from core.database import Session

# Account app models
from accounts.models import User, Otp


def hash_password(password):
    return bcrypt.hash(password)


def validate_password(db: Session, username, password):
    user = db.query(User).filter(User.username == username).one_or_none()
    if not user or user.is_active is False:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found or is not active')
    password_validation = bcrypt.verify(password, user.password)
    if password_validation:
        return True
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect password')


def generate_otpcode(db: Session, user_id):
    otp_obj = Otp(user=user_id, code=random.randint(1000, 9999))
    print('==============================')
    print(otp_obj.code)
    print('==============================')
    db.add(otp_obj)
    db.commit()
    db.refresh(otp_obj)
    return True
