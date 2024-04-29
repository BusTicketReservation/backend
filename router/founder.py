import datetime
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


@router.get("/searchTeacher", response_model=dict,
            status_code=200)
def searchTeacher(search: str, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    teacher = db.query(models.Teacher).filter(
        models.Teacher.name.like(f"%{search}%")).all()
    teacher += db.query(models.Teacher).filter(
        models.Teacher.department.like(f"%{search}%")).all()
    teacher += db.query(models.Teacher).filter(
        models.Teacher.subject.like(f"%{search}%")).all()
    teacher += db.query(models.Teacher).filter(
        models.Teacher.batch.like(f"%{search}%")).all()
    teacher += db.query(models.Teacher).filter(
        models.Teacher.college.like(f"%{search}%")).all()

    teacher += db.query(models.Teacher).filter(
        models.Teacher.university.like(f"%{search}%")).all()

    teacher += db.query(models.Teacher).filter(
        models.Teacher.email.like(f"%{search}%")).all()

    teacher += db.query(models.Teacher).filter(
        models.Teacher.phone.like(f"%{search}%")).all()

    teacher += db.query(models.Teacher).filter(
        models.Teacher.userName.like(f"%{search}%")).all()

    teacher = list(set(teacher))

    return {
        "teacher": [
            {
                "name": teacher.name,
                "batch": teacher.batch,
                "college": teacher.college,
                "university": teacher.university,
                "department": teacher.department,
                "subject": teacher.subject,
                "email": teacher.email,
                "phone": teacher.phone,
                "userName": teacher.userName,
            }
            for teacher in teacher
        ]
    }


@router.get("/searchStudent", response_model=dict,
            status_code=200)
def searchStudent(search: str, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):

    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    student = db.query(models.Student).filter(
        models.Student.name.like(f"%{search}%")).all()
    student += db.query(models.Student).filter(
        models.Student.school.like(f"%{search}%")).all()
    student += db.query(models.Student).filter(
        models.Student.college.like(f"%{search}%")).all()
    student += db.query(models.Student).filter(
        models.Student.email.like(f"%{search}%")).all()
    student += db.query(models.Student).filter(
        models.Student.phone.like(f"%{search}%")).all()
    student += db.query(models.Student).filter(
        models.Student.userName.like(f"%{search}%")).all()
    student = list(set(student))

    return {
        "student": [
            {
                "name": student.name,
                "school": student.school,
                "college": student.college,
                "email": student.email,
                "phone": student.phone,
                "userName": student.userName,
            }
            for student in student
        ]
    }


@router.delete("/deleteCourse/{courseID}", response_model=dict,
               status_code=200)
def deleteCourse(courseID: int, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):

    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")

    course = db.query(models.Courses).filter(
        models.Courses.id == courseID).first()

    if not course:

        raise HTTPException(status_code=400, detail="courseError")

    courseTeacher = db.query(models.CourseTeacher).filter(
        models.CourseTeacher.courseID == courseID).all()
    for teacher in courseTeacher:
        teacher = db.query(models.Teacher).filter(
            models.Teacher.email == teacher.teacherEmail).first()
        utils.sendEmail("Course Deleted",
                        f"Hello {teacher.name}, {course.name} has been deleted from our platform. You are no longer a teacher for this course. Thank you.", teacher.email)

    db.query(models.CourseTeacher).filter(
        models.CourseTeacher.courseID == courseID).delete()
    db.query(models.CourseFees).filter(
        models.CourseFees.courseID == courseID).delete()
    db.query(models.Courses).filter(models.Courses.id == courseID).delete()
    db.commit()

    return {"details": "DELETED"}


@router.post("/postBlog",  status_code=201)
def postBlog(blog: schemas.Blog, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    blog = models.Blog(title=blog.title, content=blog.content, author=currentUser.userName, timestamp=datetime.datetime.now(), edited=False)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    utils.sendEmail ("New Blog Post",
                    f"Hello {currentUser.name}, A new blog post {blog.title} has been posted on our platform. Thank you.", currentUser.email)
    return blog


@router.delete("/deleteBlog/{blogID}", status_code=200)
def deleteBlog(blogID: int, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    blog = db.query(models.Blog).filter(models.Blog.id == blogID).first()
    title = blog.title
    if not blog:
        raise HTTPException(status_code=400, detail="blogError")
    db.query(models.Blog).filter(models.Blog.id == blogID).delete()
    db.commit()

    utils.sendEmail("Blog Deleted",
                    f"Hello {currentUser.name}, A blog post {title} has been deleted from our platform. Thank you.", currentUser.email)

    return {"details": "DELETED"}


@router.put("/editBlog/{blogID}", status_code=200)
def editBlog(blogID: int, update: schemas.Blog, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    blog = db.query(models.Blog).filter(models.Blog.id == blogID).first()
    if not blog:
        raise HTTPException(status_code=400, detail="blogError")
    blog.title = update.title
    blog.content = update.content
    blog.edited = True
    blog.timestamp = datetime.datetime.now()
    db.commit()
    db.refresh(blog)

    utils.sendEmail("Blog Edited",
                    f"Hello {currentUser.name}, A blog post {blog.title} has been edited on our platform. Thank you.", currentUser.email)

    return blog
