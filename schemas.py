from datetime import date

from typing import List
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    accessToken: str
    token_type: str
    email:EmailStr
    role:str
    name:str
    phone:str


class TokenData(BaseModel):
    email:EmailStr


class payload(BaseModel):
    email:EmailStr
    role:str
    phone:str
    name:str
    

    class Config:
        orm_mode = True


class User(BaseModel):
    email:EmailStr
    phone:str
    name:str
    password:str
    role:str

    class Config:
        orm_mode = True

class StudentSignup(BaseModel):
    email:EmailStr
    phone:str
    name:str
    password:str
    school:str
    college:str

    class Config:
        orm_mode = True

class Student(BaseModel):
    email:EmailStr
    phone:str
    name:str
    school:str
    college:str

    class Config:
        orm_mode = True


class TeacherSignup(BaseModel):
    email:EmailStr
    phone:str
    name:str
    password:str
    batch:str
    college:str
    university:str
    department:str
    subject:str
    class Config:
        orm_mode = True

class Teacher(BaseModel):
    email:EmailStr
    phone:str
    name:str
    batch:str
    college:str
    university:str
    department:str
    subject:str
    class Config:
        orm_mode = True


class UserSignin(BaseModel):
    email:EmailStr
    password:str

    class Config:
        orm_mode = True



class FounderSignup(BaseModel):
    email:EmailStr
    phone:str
    name:str
    password:str
    position:str

    class Config:
        orm_mode = True

class Founder(BaseModel):
    email:EmailStr
    phone:str
    name:str
    position:str

    class Config:
        orm_mode = True

class StudentUpdate(BaseModel):
    name:str
    phone:str
    school:str
    college:str

    class Config:
        orm_mode = True

class TeacherUpdate(BaseModel):
    name:str
    phone:str
    batch:str
    college:str
    university:str
    department:str
    subject:str

    class Config:
        orm_mode = True


class FounderUpdate(BaseModel):
    name:str
    phone:str
    position:str

    class Config:
        orm_mode = True


#practice
    
class Remove(BaseModel):
    email:EmailStr
    class Config:
        orm_mode = True