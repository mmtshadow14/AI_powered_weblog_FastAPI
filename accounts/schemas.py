from pydantic import BaseModel, Field


# registration schema
class UserRegisterSchema(BaseModel):
    """
    with this we will get registration information from the user
    """
    username: str = Field(...)
    password: str = Field(...)


# activation schema
class UserActivateSchema(BaseModel):
    """
    with this we will get activation code from the user to authenticate the user
    """
    code: int = Field(...)


# get token schema
class GetTokenSchema(BaseModel):
    """
    with this we will get username and password from the user to authenticate the user
    and if the authentication was ok we will give the user a token to authenticate in the rest of the app
    """
    username: str = Field(...)
    password: str = Field(...)
