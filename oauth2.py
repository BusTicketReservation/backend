from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauthScheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24*60

def createAccessToken(data:dict):
    toEncode =data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp":expire})

    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

def verifyAccessToken(Token: str, credentialException):

    try:
        payload = jwt.decode(Token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str =  payload.get("id")
        if id is None:
            raise credentialException
        tokenData = schemas.TokenData(id  =  id)
    
    except JWTError:
        raise credentialException
    
    return tokenData

def getCurrentUser(token : str= Depends(oauthScheme), db: Session = Depends(database.get_db)):
    credentialException = HTTPException(status_code=404, 
                                        detail="Token is invalid",
                                        headers={"WWW-Authenticate":"Bearer"})
    
    token = verifyAccessToken(token, credentialException)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user