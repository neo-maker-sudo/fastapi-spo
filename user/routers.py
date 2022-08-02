from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from blog.database import get_db
from .models import User
from .schemas import UserSchemaIn, UserSchemaOut 

users = APIRouter(
    prefix="/users",
    tags=["users"],
)

@users.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserSchemaOut)
def get_user_view(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return user


@users.get("", status_code=status.HTTP_200_OK, response_model=List[UserSchemaOut])
def get_users_view(db: Session = Depends(get_db)):
    return db.query(User).all()


@users.post("", status_code=status.HTTP_201_CREATED, response_model=UserSchemaOut)
def create_user_view(user: UserSchemaIn, db: Session = Depends(get_db)):
    hash_pass = User.bcrypt(user.password)
    new_user = User(username=user.username, email=user.email, password=hash_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user