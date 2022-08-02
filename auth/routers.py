from tokenize import Token
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .schemas import AuthSchemaIn, Token
from .utils import create_access_token
from blog.database import get_db
from user.models import User


auth = APIRouter(
    tags=["authentication"]    
)


@auth.post("/login", response_model=Token)
def login_view(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")
    
    if not User.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
