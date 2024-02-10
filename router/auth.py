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
        raise HTTPException(status_code=400, detail="emailError")
    userName = utils.createUserName(student.name)
    while True:
        if not db.query(models.User).filter(models.User.userName == userName).first():
            break
        userName = utils.createUserName(student.name)
    student.phone = str("+88")+student.phone
    user = models.User(email=student.email, phone=student.phone, name=student.name,
                       password=utils.hash(student.password), role="STUDENT", userName=userName)
    db.add(user)
    db.commit()
    db.refresh(user)

    student = models.Student(email=student.email, phone=student.phone, name=student.name,
                             school=student.school, college=student.college, userName=userName)
    db.add(student)
    db.commit()
    db.refresh(student)

    utils.sendEmail("Welcome to our platform",
                    f"Hello {student.name}, Welcome to our platform. Your username is {userName}. You can use this username to login to our platform. Thank you.", student.email)

    return student


@router.post("/signin", response_model=schemas.Token)
def signin(
    credential: schemas.UserSignin,

    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        models.User.email == credential.email or models.User.userName == credential.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="emailError")
    if not utils.verify(credential.password, user.password):
        raise HTTPException(status_code=404, detail="passwordError")

    access_token = oauth2.createAccessToken(
        data={"email": user.email, "role": user.role, "name": user.name, "phone": user.phone, "userName": user.userName})

    tokenData = schemas.Token(name=user.name, email=user.email, role=user.role,
                              accessToken=access_token, phone=user.phone, token_type="Bearer", userName=user.userName)
    return tokenData


@router.post("/signup/founders", response_model=schemas.Founder, status_code=201)
def signup_founder(founder: schemas.FounderSignup, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == founder.email).first():
        raise HTTPException(status_code=400, detail="emailError")

    userName = utils.createUserName(founder.name)
    while True:
        if not db.query(models.User).filter(models.User.userName == userName).first():
            break
        userName = utils.createUserName(founder.name)
    founder.phone = str("+88")+founder.phone
    user = models.User(email=founder.email, phone=founder.phone, name=founder.name,
                       password=utils.hash(founder.password), role="FOUNDER", userName=userName)
    db.add(user)
    db.commit()
    db.refresh(user)

    founder = models.Founder(email=founder.email, phone=founder.phone, name=founder.name,
                             position=founder.position, userName=userName)
    db.add(founder)
    db.commit()
    db.refresh(founder)

    utils.sendEmail("Welcome to our platform",
                    f"Hello {founder.name}, Welcome to our platform. Your username is {userName}. You can use this username to login to our platform. Thank you.", founder.email)
    return founder
