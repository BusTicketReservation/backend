import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Founder"],
    prefix="/founder"
)


@router.post("/registerTeacher", response_model=schemas.Teacher, status_code=201)
def registerTeachers(teacher: schemas.TeacherSignup, db: Session = Depends(database.get_db),
                     currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    if db.query(models.User).filter(models.User.email == teacher.email).first():
        raise HTTPException(status_code=400, detail="emailError")

    userName = utils.createUserName(teacher.name)
    while True:
        if not db.query(models.User).filter(models.User.userName == userName).first():
            break
        userName = utils.createUserName(teacher.name)
    teacher.phone = str("+88")+teacher.phone
    user = models.User(email=teacher.email, phone=teacher.phone, name=teacher.name,
                       password=utils.hash(teacher.password), role="TEACHER", userName=userName)
    db.add(user)
    db.commit()
    db.refresh(user)

    teacher = models.Teacher(email=teacher.email, phone=teacher.phone, name=teacher.name,
                             batch=teacher.batch, college=teacher.college, university=teacher.university,
                             department=teacher.department, subject=teacher.subject, userName=userName)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    utils.sendEmail("Welcome to our platform",
                    f"Hello {teacher.name}, Welcome to our platform. Your username is {userName}. You can use this username to login to our platform. Thank you.", teacher.email)

    return teacher


@router.get("/profile", response_model=schemas.Founder)
def getProfile(db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER" and db.query(models.Founder).filter(models.Founder.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="emailError")
    founder = db.query(models.Founder).filter(
        models.Founder.email == currentUser.email).first()
    return founder


@router.put("/profileUpdate", response_model=schemas.Founder)
def updateProfile(updateInfo: schemas.FounderUpdate, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER" and db.query(models.Founder).filter(models.Founder.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="emailError")
    founder = db.query(models.Founder).filter(
        models.Founder.email == currentUser.email).first()
    founder.name = updateInfo.name
    founder.phone = updateInfo.phone
    db.commit()

    db.refresh(founder)

    user = db.query(models.User).filter(
        models.User.email == currentUser.email).first()
    user.name = founder.name
    user.phone = founder.phone
    db.commit()
    db.refresh(user)

    return founder


@router.post("/addCourses", response_model=dict,
             status_code=201)
def addCourses(getCourse: schemas.Course, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):

    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    course = models.Courses(name=getCourse.name, description=getCourse.description,
                            duration=getCourse.duration, startDate=getCourse.startDate)
    db.add(course)
    db.commit()
    db.refresh(course)

    courseFees = models.CourseFees(courseID=course.id, fees=getCourse.fees,
                                   discount=getCourse.discount, discountUpTo=getCourse.discountUpTo)
    db.add(courseFees)
    db.commit()
    db.refresh(courseFees)

    getTeacher = []

    for teacher in getCourse.teachersUserName:
        teacher = db.query(models.Teacher).filter(
            models.Teacher.userName == teacher).first()
        getTeacher.append(teacher)
        if not teacher:
            raise HTTPException(status_code=400, detail="userNameError")
        courseTeacher = models.CourseTeacher(
            courseID=course.id, teacherEmail=teacher.email, teacherUserName=teacher.userName)
        db.add(courseTeacher)
        db.commit()
        db.refresh(courseTeacher)

        utils.sendEmail("Course Added",
                        f"Hello {teacher.name}, A new course has been added to our platform. You are assigned as a teacher for this course. Thank you.", teacher.email)

    responseData = {
        "courseName": getCourse.name,
        "description": getCourse.description,
        "duration": getCourse.duration,
        "startDate": getCourse.startDate,
        "fees": getCourse.fees,
        "discount": getCourse.discount,
        "discountUpTo": getCourse.discountUpTo,
        "teacher": [
            {
                "name": teacher.name,
                "batch": teacher.batch,
                "college": teacher.college,
                "university": teacher.university,
                "department": teacher.department}
            for teacher in getTeacher
        ]
    }
    return responseData
