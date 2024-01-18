from datetime import date

from typing import List
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    id:int
    accessToken: str
    token_type: str
    email:EmailStr
    role:str
    name:str


class TokenData(BaseModel):
    id:int


class payload(BaseModel):
    id:int
    email:EmailStr
    role:str
    phone:str
    name:str
    dateOfBirth:date
    

    class Config:
        orm_mode = True

class CustomerSignUp(BaseModel):
    name:str
    email:EmailStr
    password:str
    phone:str
    dateOfBirth:date
    address:str
    nid:str




class CustomerOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    phone:str
    dateOfBirth:date
    address:str
    nid:str
    class Config:
        orm_mode = True


class BusSignUp(BaseModel):
    companyName:str
    email:EmailStr
    password:str
    phone:str
    licenseNo:str

class BusOut(BaseModel):
    id:int
    companyName:str
    email:EmailStr
    phone:str
    licenseNo:str
    class Config:
        orm_mode = True
    
class SignIn(BaseModel):
    email:EmailStr
    password:str


