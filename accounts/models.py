# SQLALCHEMY
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

# CORE MODELS
from core.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=func.now())
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)


class Otp(Base):
    __tablename__ = 'otps'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, ForeignKey('users.username'))
    code = Column(Integer, max_length=4)

    created_at = Column(DateTime, default=func.now())
