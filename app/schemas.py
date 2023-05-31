from datetime import datetime
from pydantic import BaseModel, EmailStr, conint, constr, validators
from typing import Optional

#>>>>>>>>>>>>>NOTTE<<<<<<<<<<<<<<<<<<
#use schemas to get the kind of information we want from the user

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    
class CreatePost(Post):
    pass

class UpdatePost(Post):
    Post.title : str

class PostLike(BaseModel):
        Post: Post
        likes: int

        class Config:
            orm_mode = True

class PostResponse(BaseModel):
    # title:str
    # content:str
    # published:bool
    # user_id:int
    # username:str
    # id:str
    # msg: str = "post created sucessfully"
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