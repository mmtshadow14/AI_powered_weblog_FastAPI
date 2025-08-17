# SQlALCHEMY
from sqlalchemy import Column, Integer, String, JSON

# CORE MODELS
from core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tags = Column(JSON)
    likes = Column(Integer, default=0)
