import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup", response_model=schemas.Student, status_code=201)
def signup(student: schemas.StudentSignup, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == student.email).first():
        raise HTTPException(status_code=400, detail="error")
    user = models.User(email=student.email, phone=student.phone, name=student.name,
                       password=utils.hash(student.password), role="STUDENT")
    db.add(user)
    db.commit()
    db.refresh(user)

    student = models.Student(email=student.email, phone=student.phone, name=student.name,
                             Class=student.Class, school=student.school, college=student.college)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.post("/signup/teacher", response_model=schemas.Teacher, status_code=201)
def signup_teacher(teacher: schemas.TeacherSignup, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == teacher.email).first():
        raise HTTPException(status_code=400, detail="error")
    user = models.User(email=teacher.email, phone=teacher.phone, name=teacher.name,
                       password=utils.hash(teacher.password), role="TEACHER")
    db.add(user)
    db.commit()
    db.refresh(user)

    teacher = models.Teacher(email=teacher.email, phone=teacher.phone, name=teacher.name,
                             batch=teacher.batch, school=teacher.school, college=teacher.college,
                             university=teacher.university, currentInsitute=teacher.currentInsitute)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


@router.post("/signin", response_model=schemas.Token)
def signin(
    credential: schemas.UserSignin,

    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        models.User.email == credential.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="error")
    if not utils.verify(credential.password, user.password):
        raise HTTPException(status_code=404, detail="error")
    access_token = oauth2.createAccessToken(data={
        "email": user.email,
        "role": user.role,
        "phone": user.phone,
        "name": user.name

    })
    tokenData = schemas.Token(name=user.name, email=user.email, role=user.role,
                              accessToken=access_token, phone=user.phone, token_type="bearer")
    return tokenData


@router.post("/signup/founders", response_model=schemas.Founder, status_code=201)
def signup_founder(founder: schemas.FounderSignup, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == founder.email).first():
        raise HTTPException(status_code=400, detail="error")
    user = models.User(email=founder.email, phone=founder.phone, name=founder.name,
                       password=utils.hash(founder.password), role="FOUNDER")
    db.add(user)
    db.commit()
    db.refresh(user)

    founder = models.Founder(email=founder.email, phone=founder.phone, name=founder.name,
                             position=founder.position)
    db.add(founder)
    db.commit()
    db.refresh(founder)
    return founder
