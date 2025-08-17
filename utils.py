# python packages
from passlib.hash import bcrypt
import random

# fastapi packages
from fastapi import Depends

# SQLALCHEMY
from sqlalchemy.orm import Session

# app models
from accounts.models import Otp
from posts.models import Like

# DB config
from core.database import get_db


def generate_hash_password(password):
    hashed_password = bcrypt.hash(password)
    return hashed_password


def verify_password(password, hashed_password):
    is_valid = bcrypt.verify(password, hashed_password)
    return is_valid


def generate_otpcode(user_id, response):
    otp_obj = Otp(user=user_id, code=random.randint(1000, 9999))
    response.set_cookie(key='user_id', value=user_id)
    print('==============================')
    print(otp_obj.code)
    print('==============================')
    return otp_obj


def check_like_status(user_id, post_id, db: Session = Depends(get_db)):
    like_relation = db.query(Like).filter(post_id=post_id, user=user_id).one_or_none()
    if like_relation:
        return like_relation
    return False
