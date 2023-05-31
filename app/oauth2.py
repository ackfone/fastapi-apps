from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, models, database
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import setting

#token frist set and user start form login page in user class
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
EXPIRE_TIME_OUT_MINUTE = int(setting.token_expire_time_minutes)

def create_access_token(data:dict):
    data_to_encode = data.copy()

    expireTime = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME_OUT_MINUTE)

    data_to_encode.update({
        "exp": expireTime
    })

    encode_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credential_exception
    
    return token_data


def validate_current_user(token: str =  Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Session Expired...Please Login to contiune", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.email == token.id).first()

    return user