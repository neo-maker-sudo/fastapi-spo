from typing import List
from pydantic import BaseModel
from blog.schemas import BlogSchemaOut

class UserSchemaIn(BaseModel):
    username: str
    email: str
    password: str


class UserSchemaOut(BaseModel):
    username: str
    email: str
    blogs: List["BlogSchemaOut"] = []

    class Config():
        orm_mode = True
