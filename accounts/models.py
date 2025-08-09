# SQLALCHEMY
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

# CORE MODELS
from core.database import Base


# user model
class User(Base):
    """
    this is the model that we use in out app to store user's information.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=func.now())
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)


# otp model
class Otp(Base):
    """
    with this model we will store the OTP to use it when we want to activate the user.
    """
    __tablename__ = 'otps'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, ForeignKey('users.username'))
    code = Column(Integer)

    created_at = Column(DateTime, default=func.now())
