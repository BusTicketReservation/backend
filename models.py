
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from sqlalchemy import DateTime


class User(Base):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, primary_key=True)
    phone = Column(String)
    name = Column(String)
    password = Column(String)
    role = Column(String)
    userName = Column(String, unique=True, index=True)


class Teacher(Base):
    __tablename__ = "teachers"
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    phone = Column(String)
    name = Column(String)
    batch = Column(String)
    college = Column(String)
    university = Column(String)
    department = Column(String)
    subject = Column(String)
    userName = Column(String)


class Student(Base):
    __tablename__ = "students"
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    phone = Column(String)
    name = Column(String)
    school = Column(String)
    college = Column(String)
    userName = Column(String)


class Founder(Base):
    __tablename__ = "founders"
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    phone = Column(String)
    name = Column(String)
    position = Column(String)
    userName = Column(String)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, ForeignKey("users.email"))
    receiver = Column(String, ForeignKey("users.email"))
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    duration = Column(String)
    startDate = Column(DateTime)


class CourseFees(Base):
    __tablename__ = "courseFees"
    courseID = Column(Integer, ForeignKey("courses.id"),
                      primary_key=True, index=True)
    fees = Column(Integer)
    discount = Column(Integer)
    discountUpTo = Column(DateTime)


class CourseEnrollment(Base):
    __tablename__ = "courseEnrollments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    courseID = Column(Integer, ForeignKey("courses.id"))
    studentEmail = Column(String, ForeignKey("students.email"))
    studentUserName = Column(String)
    enrollmentDate = Column(DateTime, default=datetime.utcnow)


class CourseTeacher(Base):
    __tablename__ = "courseTeachers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    courseID = Column(Integer, ForeignKey("courses.id"))
    teacherEmail = Column(String, ForeignKey("teachers.email"))
    teacherUserName = Column(String)
