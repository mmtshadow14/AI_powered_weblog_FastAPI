from pydantic import BaseModel, Field


class UserRegisterSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
