
from database import Base
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)
    role = Column(String)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dateOfBirth = Column(String)
    address = Column(String)
    nid = Column(String)
    userID = Column(Integer, ForeignKey('users.id'))
   

class Bus(Base):
    __tablename__ = 'bus'
    id = Column(Integer, primary_key=True, index=True)
    companyName = Column(String)
    licenseNo = Column(String)
    userID = Column(Integer, ForeignKey('users.id'))



   

    


    

