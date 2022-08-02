from fastapi import FastAPI
from blog.database import engine
from blog.models import Base
from user.routers import users
from blog.routers import blogs
from auth.routers import auth

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def index():
    return {"Hello": "World"}

app.include_router(auth)
app.include_router(users)
app.include_router(blogs)





