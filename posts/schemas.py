from pydantic import BaseModel, Field


class create_post_schemas(BaseModel):
    title: str = Field()
    description: str = Field()
