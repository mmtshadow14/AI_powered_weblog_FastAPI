# Python packages
import jwt
import datetime
import time

# FastAPI models
from fastapi import HTTPException, status

# Core models
from core.config import settings

# DB
from core.database import Session

# Accounts models
from accounts.models import User

# DB instance
db = Session()


# create a JWT token
def generate_jwt_token(username):
    """
    we will generate a JWT token for the user with placing his account ID in the payload of the JWT token.
    """
    pyload = {
        'username': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(pyload, settings.JWT_SECRET_KEY, algorithm='HS256')


# retrieve the user
def retrieve_user_via_jwt(token):
    """
    retrieve the user from the JWT token that is sent in the head of the request to use it in the routes
     to do CRUD operations.
    """
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
    if payload['exp'] < int(time.time()):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Token expired')
    user = db.query(User).filter(User.username == payload['username']).one_or_none()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')