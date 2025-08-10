from fastapi import Depends, HTTPException, Response, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token: str = Depends(oauth_schema), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate token", 
                                         headers={"WWW-Authenticate": "Bearer"})
    user_token = verify_access_token(token,credential_exception)
    # print(user_token.id)
    user_data = db.query(models.User).filter(models.User.id == int(user_token.id)).first()
    # print(user_data.email)
    return user_data
