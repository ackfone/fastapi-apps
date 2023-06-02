from datetime import datetime
from pydantic import BaseModel, EmailStr, conint, constr, validators
from typing import Optional

#>>>>>>>>>>>>>NOTTE<<<<<<<<<<<<<<<<<<
#use schemas to get the kind of information we want from the user

class Base(BaseModel):
    title:str
    content:str
    published:bool = True
    
class CreatePost(Base):
    pass

class UpdatePost(Base):
    Base.title : str

class PostLike(BaseModel):
        post: Base
        likes: int

        class Config:
            orm_mode = True

class PostResponse(BaseModel):
    # likes:str
    # Post:dict
    # title:str
    # content:str
    # published:bool
    # user_id:int
    # username:str
    # id:str
    # created:datetime
    class Config:
        orm_mode = True

class UserRegistraionResponse(BaseModel):
    # email:str
    # passwordt:str
    # username:str
    msg: str = "Account Created Sucessfully"
    # created:datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email:EmailStr
    password:str
    username:constr(min_length=4)


class UserExistResponse(BaseModel):
    # id:str
    username:str
    email:str
    # password:str
    # created:datetime
    # msg: str = "user exist"

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class TokenData(BaseModel):
    id:Optional[str] = None

class LikeData(BaseModel):
    post_id:int
    like_type:int = 0, conint(le=1)