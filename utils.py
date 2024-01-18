from datetime import date, timedelta,datetime
from enum import Enum
import models, database
from passlib.context import CryptContext
pwdContext = CryptContext(schemes=["bcrypt"], deprecated ="auto")
import logging,httpx
from fastapi import Depends

logging.basicConfig(level=logging.INFO)

def hash(password:str):
    return pwdContext.hash(password)

def verify(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)
