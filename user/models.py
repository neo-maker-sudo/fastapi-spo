from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from blog.database import Base
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="author")

    @staticmethod
    def bcrypt(password):
        return pwd_cxt.hash(password)
    
    @staticmethod
    def verify(plain_password, hash_password):
        return pwd_cxt.verify(plain_password, hash_password)