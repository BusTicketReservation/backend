
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, primary_key=True)
    phone = Column(String)
    name = Column(String)
    password = Column(String)
    role = Column(String)

class Teacher(Base):
    __tablename__ = "teachers"
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    phone = Column(String)
    name = Column(String)
    batch = Column(String)
    school = Column(String)
    college = Column(String)
    university = Column(String)
    currentInsitute = Column(String)
   



class Student(Base):
    __tablename__ = "students"
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    phone = Column(String)
    name = Column(String)
    Class = Column(String)
    school = Column(String)
    college = Column(String)

    