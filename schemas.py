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
    id:int


class payload(BaseModel):
    id:int
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
    Class:str
    school:str
    college:str

    class Config:
        orm_mode = True

class Student(BaseModel):
    email:EmailStr
    phone:str
    name:str
    Class:str
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
    school:str
    college:str
    university:str
    currentInsitute:str
    class Config:
        orm_mode = True

class Teacher(BaseModel):
    email:EmailStr
    phone:str
    name:str
    batch:str
    school:str
    college:str
    university:str
    currentInsitute:str
    class Config:
        orm_mode = True


class UserSignin(BaseModel):
    email:EmailStr
    password:str

    class Config:
        orm_mode = True