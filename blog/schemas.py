from typing import Optional
from pydantic import BaseModel

class BlogSchemaIn(BaseModel):
    title: str
    content: str


class BlogSchemaOut(BaseModel):
    content: str
    author_id: int


    class Config():
        orm_mode = True
