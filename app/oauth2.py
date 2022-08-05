from jose import JWTError ,jwt
from  datetime import datetime , timedelta
from sqlalchemy.orm import Session
from jose.constants import Algorithms 
from . import schemas , database , models
from fastapi import FastAPI ,Response , status , Depends ,HTTPException
from fastapi.security import OAuth2PasswordBearer
from.config import settings


Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")   #endpoint

SECRET_KEY = settings.secret_key 
ALGORITHIM = settings.algorithm 
ACCESS_TOKEN_EXPIRE_MINUTE = settings.access_token_expire_minutes

# creating a acces token
def create_acces_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY, algorithm=ALGORITHIM)
    return encoded_jwt



# verifying the acces token
def verify_acces_token(token : str , credential_exception):
 try:
    payload = jwt.decode(token ,SECRET_KEY , algorithms=[ALGORITHIM] )
    id :str = payload.get("user_id")

    if id is None:
        raise credential_exception 
    token_data =schemas.TokenData(id =id)  
 except JWTError:
     raise credential_exception
 return token_data



def get_current_user ( token :str =Depends(Oauth2_scheme) , db : Session = Depends(database.get_db) ):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED ,
                                      detail = f"could not validate credentials" , headers={"WWW-Authenticate" : "Bearer"})


    token = verify_acces_token( token , credential_exception)
    user = db.query(models.User).filter(models.User.id ==token.id).first()

    return user

    
      