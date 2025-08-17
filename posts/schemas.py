from pydantic import BaseModel, Field


class create_post_schemas(BaseModel):
    title: str = Field()
    description: str = Field()


class get_post_schemas(BaseModel):
    id: int
    user: int
    title: str
    description: str
    tags: list[str]
    likes: int
