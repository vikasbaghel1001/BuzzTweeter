from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, session
from ..database import get_db 
from .. import   schemas , models ,utils , oauth2


router = APIRouter(tags =['Authentication'])

@router.post("/login" , response_model=schemas.Token)
def login(user_crediantials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)) :
   user =  db.query(models.User).filter(models.User.email == user_crediantials.username ).first()
   if not user :
       raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , 
                                    detail = f"Invalid Credentials") 

   if not utils.verify( user_crediantials.password , user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , 
                                    detail = f"Invalid Credentials")


   # create a token 
   # return token
   access_token = oauth2.create_acces_token(data = {"user_id" : user.id})
   return { "access_token" : access_token , "token_type" : "bearer"}

