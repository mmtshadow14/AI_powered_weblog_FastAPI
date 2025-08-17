from pydantic import BaseModel, Field


# create post schema
class create_post_schemas(BaseModel):
    """
    with this schema we will get information from the user and use it in create post.
    """
    title: str = Field()
    description: str = Field()


# get post schema
class get_post_schemas(BaseModel):
    """
    with this schema we will serialize the posts we want to show the user.
    """
    id: int
    user: int
    title: str
    description: str
    tags: list[str]
    likes: int
