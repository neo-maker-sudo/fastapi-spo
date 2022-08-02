from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Blog
from .schemas import BlogSchemaIn, BlogSchemaOut
from .database import get_db
from user.models import User
from auth.utils import get_current_user

blogs = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)

@blogs.get("", status_code=status.HTTP_200_OK, response_model=List[BlogSchemaOut])
def get_blogs_view(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Blog).all()
    

@blogs.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogSchemaOut)
def get_blog_view(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found"
        )

    return blog


@blogs.post("", status_code=status.HTTP_201_CREATED, response_model=BlogSchemaOut)
def create_blog_view(blog: BlogSchemaIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_blog = Blog(title=blog.title, content=blog.content, author_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@blogs.put("/{id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT, response_model=BlogSchemaOut)
def update_blog_view(id: int, blog: BlogSchemaIn, db: Session = Depends(get_db)):
    qs = db.query(Blog).filter(Blog.id == id)

    if not qs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")

    qs.update(blog.dict(), synchronize_session=False)
    db.commit()

    return blog


@blogs.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_view(id: int, db: Session = Depends(get_db)):
    qs = db.query(Blog).filter(Blog.id == id)
    
    if not qs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
    
    qs.delete(synchronize_session=False)
    db.commit()

    return