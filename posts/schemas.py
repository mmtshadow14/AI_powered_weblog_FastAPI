from pydantic import BaseModel, Field


class create_post_schemas(BaseModel):
    title: str = Field()
    description: str = Field()


class get_post_schemas(BaseModel):
    id: int = Field()
    user: int = Field()
    title: str = Field()
    description: str = Field()
    tags = list[str]
    likes = int = Field()
