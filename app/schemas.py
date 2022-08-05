from pydantic import BaseModel , EmailStr
from pydantic.types import  conint
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id : int 
    email : EmailStr
    name :str
    created_at: datetime 

    class Config:
        orm_mode = True 



class Post(BaseModel):
    title : str
    content : str
    published : bool = True



class Post2(Post) :
  id :int
  created_at: datetime            # inheritance from post
  owner_id : int
  owner : UserOut
  
  class Config:
        orm_mode = True   
    




class UserCreate(BaseModel):
       name : str
       email: EmailStr
       password :str  



class UserLogin(BaseModel):
    email:EmailStr
    password : str       



class Token(BaseModel):
    access_token : str
    token_type : str

    class Config:
        orm_mode = True 



class TokenData(BaseModel):
   id : Optional[str] = None


class Vote(BaseModel):
    post_id :int
    dir : conint(le=1)
     
    
